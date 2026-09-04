"""CLI proxy for the interactive redis-cli widget in the docs.

The browser (static/js/cli.js) POSTs a batch of commands to /cli; this service
runs them against the sidecar Redis and returns replies tagged with their RESP
type so the frontend can render them byte-for-byte like the native redis-cli:

  * simple-string replies (+OK, +PONG)  -> {"value": "OK", "status": true}  (no quotes)
  * bulk-string replies   ($...)        -> {"value": "<text>"}              (quoted)
  * integer replies       (:...)        -> {"value": 42} or {"value": {"$int": "..."}}
  * error replies         (-ERR ...)    -> {"error": true, "value": "<msg>"}

RESP is parsed directly off the socket because high-level clients collapse the
simple/bulk distinction into a plain string and lose the type we need here.
RESP3 replies (after HELLO 3) are mapped back onto these RESP2-shaped values.
"""

import logging
import os
import shlex
import socket
import threading
import time
import uuid
from collections import OrderedDict
from collections.abc import Callable
from dataclasses import dataclass, field

from flask import Flask, jsonify, request

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
LOGGER = logging.getLogger("cli_proxy")

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))
SOCKET_TIMEOUT = float(os.environ.get("REDIS_TIMEOUT", "5"))

# The restricted user from sandbox.acl. Everything a reader types runs as this
# user, which is what stops FLUSHALL and friends. Empty means connect
# unauthenticated, for a Redis started without the ACL file.
REDIS_USERNAME = os.environ.get("REDIS_USERNAME", "")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "")

# RESET carries Redis's no-auth flag, so no ACL rule can deny it: `ACL SETUSER
# -reset` is accepted and ACL DRYRUN still passes the command. Left alone it
# would drop the connection back to the default user mid-session, which both
# undoes the sandbox user and discards the MULTI or WATCH the reader is in the
# middle of. Nothing in the docs runs it, so the proxy refuses it here.
PROXY_DENIED = frozenset({"RESET"})

# Sessions are sticky (see SessionRegistry) so they have to be bounded, or every
# visitor's connection is held for the life of the process. A session goes when
# it has been idle this long, and the oldest go early if the cap is reached
# first; either way the reader just gets a fresh session on their next command.
SESSION_IDLE_TTL = float(os.environ.get("SESSION_IDLE_TTL", "1800"))
SESSION_MAX = int(os.environ.get("SESSION_MAX", "500"))
# Idle sessions are swept on the way into a request rather than by a background
# thread: an idle process has nothing to collect, and this keeps the sidecar to
# the one thread pool gunicorn already runs.
SWEEP_INTERVAL = float(os.environ.get("SESSION_SWEEP_INTERVAL", "60"))

# Integers beyond this magnitude lose precision once serialized as JSON numbers
# and parsed by the browser, so they are tagged {"$int": "<decimal>"} instead.
JS_MAX_SAFE_INTEGER = 2**53 - 1

CRLF = b"\r\n"


class RespProtocolError(Exception):
    """The server sent bytes that do not conform to the RESP grammar."""


class RedisAuthError(Exception):
    """Redis refused the sandbox user's credentials."""


class RespStatus(str):
    """A RESP simple-string reply (+...), tagged so the frontend drops the quotes."""


class RespError(str):
    """A RESP error reply (-...), carrying the human-readable message."""


class RespConnection:
    """A single buffered RESP2/RESP3 connection to Redis over a raw TCP socket."""

    def __init__(self, host: str, port: int, timeout: float) -> None:
        self._socket = socket.create_connection((host, port), timeout=timeout)
        self._buffer = b""

    def send_command(self, args: list[str]) -> None:
        chunks = [b"*%d\r\n" % len(args)]
        for arg in args:
            raw = arg.encode("utf-8")
            chunks.append(b"$%d\r\n" % len(raw))
            chunks.append(raw)
            chunks.append(CRLF)
        self._socket.sendall(b"".join(chunks))

    def read_reply(self) -> object:
        line = self._read_line()
        prefix, payload = line[:1], line[1:]

        if prefix == b"+":
            return RespStatus(payload.decode("utf-8", "replace"))
        if prefix == b"-":
            return RespError(payload.decode("utf-8", "replace"))
        if prefix in (b":", b"("):  # RESP2 integer / RESP3 big number
            return self._as_number(payload)
        if prefix == b"$" or prefix == b"=":  # bulk string / RESP3 verbatim string
            return self._read_bulk_string(self._parse_count(payload), verbatim=prefix == b"=")
        if prefix in (b"*", b"~", b">"):  # array / RESP3 set / RESP3 push
            return self._read_array(self._parse_count(payload))
        if prefix == b"%":  # RESP3 map -> flat [k, v, ...] list, matching redis-cli
            return self._read_array(self._parse_count(payload) * 2)
        if prefix == b"|":  # RESP3 attribute: discard the metadata, return the real reply
            self._read_array(self._parse_count(payload) * 2)
            return self.read_reply()
        if prefix == b"#":  # RESP3 boolean -> integer 1/0, matching the proxy's RESP2 contract
            return 1 if payload == b"t" else 0
        if prefix == b",":  # RESP3 double
            return self._as_number(payload)
        if prefix == b"_":  # RESP3 null
            return None
        raise RespProtocolError(f"unexpected RESP prefix: {prefix!r}")

    def close(self) -> None:
        try:
            self._socket.close()
        except OSError as error:
            LOGGER.debug("ignoring error while closing socket: %s", error)

    def _read_bulk_string(self, length: int, verbatim: bool) -> str | None:
        if length == -1:
            return None
        text = self._read_exact(length).decode("utf-8", "replace")
        # RESP3 verbatim strings are prefixed with a 3-char format tag, e.g. "txt:".
        if verbatim and len(text) >= 4 and text[3] == ":":
            return text[4:]
        return text

    def _read_array(self, count: int) -> list | None:
        if count == -1:
            return None
        return [self.read_reply() for _ in range(count)]

    def _as_number(self, payload: bytes) -> object:
        text = payload.decode("ascii", "replace")
        try:
            return int(text)
        except ValueError:
            return float(text)  # RESP3 double

    def _parse_count(self, payload: bytes) -> int:
        try:
            return int(payload.decode("ascii"))
        except ValueError as error:
            raise RespProtocolError(f"invalid RESP length: {payload!r}") from error

    def _read_line(self) -> bytes:
        while CRLF not in self._buffer:
            self._fill()
        line, self._buffer = self._buffer.split(CRLF, 1)
        return line

    def _read_exact(self, length: int) -> bytes:
        while len(self._buffer) < length + len(CRLF):
            self._fill()
        data = self._buffer[:length]
        self._buffer = self._buffer[length + len(CRLF):]
        return data

    def _fill(self) -> None:
        chunk = self._socket.recv(4096)
        if not chunk:
            raise RespProtocolError("redis closed the connection")
        self._buffer += chunk


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


class SessionRegistry:
    """The live sessions, ordered least-recently-used first.

    A session keeps a connection of its own rather than borrowing one from a
    pool, because connection state a reader builds up has to survive between
    requests: cli.js POSTs each typed command as its own batch, so MULTI and
    EXEC — or WATCH and the command it guards — arrive as separate HTTP calls
    and only reach the same Redis client if the session is sticky.

    That stickiness is why the registry is bounded. Nothing about a browser
    session tells us when the reader closed the tab, so a session is abandoned
    once it goes quiet, and the cap catches the rest.
    """

    def __init__(
        self,
        connect: Callable[[], RespConnection],
        max_sessions: int = SESSION_MAX,
        idle_ttl: float = SESSION_IDLE_TTL,
        sweep_interval: float = SWEEP_INTERVAL,
    ) -> None:
        self._connect = connect
        # Never below one, or the cap reclaims the session acquire just opened
        # and hands back a closed connection that can only fail and reconnect.
        self._max_sessions = max(1, max_sessions)
        self._idle_ttl = idle_ttl
        self._sweep_interval = sweep_interval
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

        _close_all(overflow)
        if overflow:
            LOGGER.warning("session cap %d reached, closed %d", self._max_sessions, len(overflow))
        LOGGER.info("opened redis session %s (%d live)", sid, live)
        return session, sid

    def sweep(self) -> None:
        """Close sessions that have gone quiet, at most once per sweep interval."""
        now = time.monotonic()
        with self._lock:
            if now - self._last_sweep < self._sweep_interval:
                return
            self._last_sweep = now
            expired = self._reclaim(lambda session: now - session.last_seen >= self._idle_ttl)

        _close_all(expired)
        if expired:
            LOGGER.info("closed %d idle session(s)", len(expired))

    def discard(self, sid: str) -> None:
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


def _close_all(sessions: list[Session]) -> None:
    for session in sessions:
        session.connection.close()


def _open_connection() -> RespConnection:
    connection = RespConnection(REDIS_HOST, REDIS_PORT, SOCKET_TIMEOUT)
    if REDIS_USERNAME:
        authenticate(connection, REDIS_USERNAME, REDIS_PASSWORD)
    return connection


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


_registry = SessionRegistry(_open_connection)


def encode_value(value: object) -> object:
    """Make a parsed RESP value JSON-safe for the frontend's formatReply."""
    if isinstance(value, RespError):
        return f"(error) {value}"
    if isinstance(value, RespStatus):
        return str(value)
    if isinstance(value, bool):
        return value
    if isinstance(value, int) and abs(value) > JS_MAX_SAFE_INTEGER:
        return {"$int": str(value)}
    if isinstance(value, list):
        return [encode_value(item) for item in value]
    return value


def run_command(session: Session, command: str) -> dict:
    try:
        argv = shlex.split(command)
    except ValueError as error:
        return {"error": True, "value": f"parse error: {error}"}
    if not argv:
        return {"error": True, "value": "empty command"}
    if argv[0].upper() in PROXY_DENIED:
        # Phrased the way Redis phrases an ACL refusal, so the widget renders it
        # like any other denied command rather than like a proxy malfunction.
        return {
            "error": True,
            "value": f"NOPERM this user has no permissions to run the '{argv[0].lower()}' command",
        }

    session.connection.send_command(argv)
    reply = session.connection.read_reply()

    if isinstance(reply, RespError):
        return {"error": True, "value": str(reply)}
    if isinstance(reply, RespStatus):
        return {"error": False, "value": str(reply), "status": True}
    return {"error": False, "value": encode_value(reply)}


app = Flask(__name__)


@app.route("/healthz")
def healthz() -> str:
    return "ok"


@app.route("/cli", methods=["POST"])
def cli():
    body = request.get_json(silent=True) or {}
    commands = body.get("commands", [])
    session_id = body.get("id")

    _registry.sweep()

    try:
        session, sid = _registry.acquire(session_id)
    except OSError as error:
        LOGGER.error("could not reach redis: %s", error)
        replies = [{"error": True, "value": "could not connect to redis"} for _ in commands]
        return jsonify({"replies": replies, "id": session_id or ""})
    except RedisAuthError as error:
        LOGGER.error("redis rejected the sandbox user %r: %s", REDIS_USERNAME, error)
        replies = [{"error": True, "value": "could not connect to redis"} for _ in commands]
        return jsonify({"replies": replies, "id": session_id or ""})

    replies: list[dict] = []
    with session.lock:
        for index, command in enumerate(commands):
            try:
                replies.append(run_command(session, command))
            except (OSError, RespProtocolError) as error:
                LOGGER.error("redis failure on session %s: %s", sid, error)
                _registry.discard(sid)
                replies.extend(
                    {"error": True, "value": "redis connection lost, please retry"}
                    for _ in commands[index:]
                )
                break

    return jsonify({"replies": replies, "id": sid})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8090")))