"""Who is connected, for how long, and what they leave behind.

A session keeps a Redis connection of its own rather than borrowing one from a
pool, because connection state a reader builds up has to survive between
requests: cli.js POSTs each typed command as its own batch, so MULTI and EXEC —
or WATCH and the command it guards — arrive as separate HTTP calls and only
reach the same Redis client if the session is sticky.

That stickiness is why the registry is bounded, and why reclaiming a session is
more than closing a socket: the keys and indexes it created are still in the
shared database, under its prefix, with nothing left to reach them.
"""

import logging
import threading
import time
import uuid
from collections import OrderedDict
from collections.abc import Callable
from dataclasses import dataclass, field

from namespace import Namespace
from resp import RespConnection, RespError, RespProtocolError

LOGGER = logging.getLogger("cli_proxy.sessions")


class RedisAuthError(Exception):
    """Redis refused the sandbox user's credentials."""


def authenticate(connection: RespConnection, username: str, password: str) -> None:
    """Log the connection in as the sandbox user, or close it and give up.

    A connection that stays on the default user would run a reader's commands
    with full rights, so a refused AUTH has to end the connection rather than
    quietly fall through to one that can still run FLUSHALL.
    """
    connection.send_command(["AUTH", username, password])
    reply = connection.read_reply()
    if isinstance(reply, RespError):
        connection.close()
        raise RedisAuthError(str(reply))


@dataclass
class Session:
    """One browser session: its Redis connection, and when it was last used.

    The lock serializes the worker threads sharing the connection; last_seen is
    what the registry's sweep reads to decide the session has been abandoned.
    """

    sid: str
    connection: RespConnection
    lock: threading.Lock = field(default_factory=threading.Lock)
    last_seen: float = field(default_factory=time.monotonic)

    @property
    def namespace(self) -> Namespace:
        return Namespace(self.sid)


class SessionJanitor:
    """Deletes what a reclaimed session left in the shared database.

    Runs on the session's own connection, before it is closed, so it needs no
    connection of its own and inherits the sandbox user's rights — which is also
    why it can only reach keys under that session's prefix.

    Indexes go first. Dropping an index after its documents leaves RediSearch
    holding a definition over keys that no longer exist, and FT._LIST would still
    answer with it for whoever inherits nothing.
    """

    def __init__(self, batch: int, scan_count: int) -> None:
        self._batch = batch
        self._scan_count = scan_count

    def clean(self, session: Session) -> int:
        namespace = session.namespace
        try:
            # A session reclaimed with a MULTI still open answers QUEUED to
            # everything, so the cleanup would queue itself into a transaction
            # that is then thrown away with the connection. Close it first.
            session.connection.send_command(["DISCARD"])
            session.connection.read_reply()
            self._drop_indexes(session, namespace)
            return self._delete_keys(session, namespace)
        except (OSError, RespProtocolError) as error:
            # Cleanup runs while a session is being thrown away, and every path
            # out of here ends in the socket being closed. A failure means some
            # keys outlive their session, which is untidy; letting it propagate
            # would mean the socket leaks instead, which is worse.
            LOGGER.warning("could not clean up session %s: %s", session.sid, error)
            return 0

    def _drop_indexes(self, session: Session, namespace: Namespace) -> None:
        session.connection.send_command(["FT._LIST"])
        reply = session.connection.read_reply()
        if not isinstance(reply, list):
            return
        for name in reply:
            if isinstance(name, str) and namespace.owns(name):
                session.connection.send_command(["FT.DROPINDEX", name])
                session.connection.read_reply()

    def _delete_keys(self, session: Session, namespace: Namespace) -> int:
        deleted = 0
        cursor = "0"
        while True:
            session.connection.send_command(
                ["SCAN", cursor, "MATCH", namespace.prefix + "*", "COUNT", str(self._scan_count)]
            )
            reply = session.connection.read_reply()
            if not isinstance(reply, list) or len(reply) != 2:
                return deleted

            cursor = str(reply[0])
            keys = [k for k in reply[1] if isinstance(k, str)]
            for start in range(0, len(keys), self._batch):
                chunk = keys[start:start + self._batch]
                session.connection.send_command(["DEL", *chunk])
                session.connection.read_reply()
                deleted += len(chunk)

            if cursor == "0":
                return deleted


class SessionRegistry:
    """The live sessions, ordered least-recently-used first.

    Nothing about a browser session tells us when the reader closed the tab, so
    a session is abandoned once it goes quiet, and the cap catches the rest.
    """

    def __init__(
        self,
        connect: Callable[[], RespConnection],
        max_sessions: int,
        idle_ttl: float,
        sweep_interval: float,
        janitor: SessionJanitor | None = None,
    ) -> None:
        self._connect = connect
        # Never below one, or the cap reclaims the session acquire just opened
        # and hands back a closed connection that can only fail and reconnect.
        self._max_sessions = max(1, max_sessions)
        self._idle_ttl = idle_ttl
        self._sweep_interval = sweep_interval
        self._janitor = janitor
        self._sessions: OrderedDict[str, Session] = OrderedDict()
        self._lock = threading.Lock()
        self._last_sweep = time.monotonic()

    def acquire(self, session_id: str | None) -> tuple[Session, str]:
        sid = session_id or str(uuid.uuid4())

        with self._lock:
            session = self._touch(sid)
        if session is not None:
            return session, sid

        # Connect outside the lock so a slow or unreachable Redis never stalls
        # every other worker thread.
        connection = self._connect()

        with self._lock:
            existing = self._touch(sid)
            if existing is not None:
                connection.close()
                return existing, sid
            session = Session(sid=sid, connection=connection)
            self._sessions[sid] = session
            overflow = self._reclaim(lambda _: len(self._sessions) > self._max_sessions)
            live = len(self._sessions)

        self._retire(overflow)
        if overflow:
            LOGGER.warning("session cap %d reached, closed %d", self._max_sessions, len(overflow))
        LOGGER.info("opened redis session %s (%d live)", sid, live)
        return session, sid

    def sweep(self) -> None:
        """Reclaim sessions that have gone quiet, at most once per interval."""
        now = time.monotonic()
        with self._lock:
            if now - self._last_sweep < self._sweep_interval:
                return
            self._last_sweep = now
            expired = self._reclaim(lambda session: now - session.last_seen >= self._idle_ttl)

        self._retire(expired)
        if expired:
            LOGGER.info("reclaimed %d idle session(s)", len(expired))

    def discard(self, sid: str) -> None:
        """Drop a session whose connection has already failed.

        No cleanup: the connection cleanup would run on is the broken one.
        """
        with self._lock:
            session = self._sessions.pop(sid, None)
        if session is not None:
            session.connection.close()
            LOGGER.warning("dropped redis session %s", sid)

    def __len__(self) -> int:
        with self._lock:
            return len(self._sessions)

    def _touch(self, sid: str) -> Session | None:
        """Mark a session used and move it to the young end. Caller holds the lock."""
        session = self._sessions.get(sid)
        if session is None:
            return None
        session.last_seen = time.monotonic()
        self._sessions.move_to_end(sid)
        return session

    def _reclaim(self, should_close: Callable[[Session], bool]) -> list[Session]:
        """Take out the oldest sessions the predicate still accepts.

        Caller holds the lock; the connections are closed outside it. A session
        another thread is mid-batch on is left alone — it is in use, so it is
        neither idle nor the right one to sacrifice to the cap.
        """
        reclaimed: list[Session] = []
        for sid in list(self._sessions):
            session = self._sessions[sid]
            if not should_close(session):
                break  # ordered oldest first, so nothing further qualifies
            if not session.lock.acquire(blocking=False):
                continue
            del self._sessions[sid]
            session.lock.release()
            reclaimed.append(session)
        return reclaimed

    def _retire(self, sessions: list[Session]) -> None:
        for session in sessions:
            if self._janitor is not None:
                deleted = self._janitor.clean(session)
                if deleted:
                    LOGGER.info("session %s left %d key(s), deleted", session.sid, deleted)
            session.connection.close()
