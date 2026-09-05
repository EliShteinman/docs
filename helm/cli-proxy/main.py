"""CLI proxy for the interactive redis-cli widget in the docs.

The browser (static/js/cli.js) POSTs a batch of commands to /cli; this service
runs each one against the sidecar Redis and returns the replies tagged with
their RESP type, so the widget can render them byte-for-byte like the native
redis-cli. resp.py does that parsing.

Everyone shares one Redis database, so a command does not go out as the reader
typed it: namespace.py rewrites it into that session's own slice of the keyspace
and takes the namespace back off the reply. sessions.py decides how long a
session lives and cleans up after it. files/sandbox.acl, mounted into the Redis
sidecar, is what stops the commands neither of those can make safe.
"""

import logging
import shlex
import threading

from flask import Flask, jsonify, request

import config
from namespace import (
    LOOKUP_UNAVAILABLE,
    CommandRewriter,
    KeyLookupUnavailable,
    KeyResolver,
    Namespace,
    ReplyFilter,
)
from resp import RespConnection, RespError, RespProtocolError, RespStatus, encode_value
from sessions import RedisAuthError, Session, SessionJanitor, SessionRegistry, authenticate

logging.basicConfig(
    level=config.LOG_LEVEL,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
LOGGER = logging.getLogger("cli_proxy")

# RESET carries Redis's no-auth flag, so no ACL rule can deny it: `ACL SETUSER
# -reset` is accepted and ACL DRYRUN still passes the command. Left alone it
# would drop the connection back to the default user mid-session, which both
# undoes the sandbox user and discards the MULTI or WATCH the reader is in the
# middle of. Nothing in the docs runs it, so the proxy refuses it here.
PROXY_DENIED = frozenset({"RESET"})


def open_connection() -> RespConnection:
    connection = RespConnection(config.REDIS_HOST, config.REDIS_PORT, config.SOCKET_TIMEOUT)
    if config.REDIS_USERNAME:
        authenticate(connection, config.REDIS_USERNAME, config.REDIS_PASSWORD)
    return connection


class LookupConnection:
    """A connection kept aside for COMMAND GETKEYS, reconnecting when it breaks.

    Key lookups cannot share a session's connection — a session inside MULTI
    answers QUEUED to everything — so they get one of their own, serialized by a
    lock. One is enough: a lookup is a single round trip to a socket in the same
    pod.
    """

    def __init__(self, connect) -> None:
        self._connect = connect
        self._connection: RespConnection | None = None
        self._lock = threading.Lock()

    def execute(self, argv: list[str]) -> object:
        with self._lock:
            for attempt in (1, 2):
                try:
                    if self._connection is None:
                        self._connection = self._connect()
                    self._connection.send_command(argv)
                    return self._connection.read_reply()
                except (OSError, RespProtocolError, RedisAuthError) as error:
                    self._drop()
                    if attempt == 2:
                        LOGGER.warning("key lookup failed for %s: %s", argv[:2], error)
                        return RespError(LOOKUP_UNAVAILABLE)
            return RespError(LOOKUP_UNAVAILABLE)

    def _drop(self) -> None:
        if self._connection is not None:
            self._connection.close()
            self._connection = None


_lookup = LookupConnection(open_connection)
_rewriter = CommandRewriter(KeyResolver(_lookup.execute), config.SCAN_MIN_COUNT)
_replies = ReplyFilter()
_janitor = (
    SessionJanitor(config.CLEANUP_BATCH, config.SCAN_MIN_COUNT)
    if config.CLEANUP_ENABLED and config.NAMESPACE_ENABLED
    else None
)
_registry = SessionRegistry(
    open_connection,
    max_sessions=config.SESSION_MAX,
    idle_ttl=config.SESSION_IDLE_TTL,
    sweep_interval=config.SWEEP_INTERVAL,
    janitor=_janitor,
)


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

    namespace: Namespace | None = session.namespace if config.NAMESPACE_ENABLED else None
    try:
        outgoing = _rewriter.rewrite(argv, namespace) if namespace else argv
    except KeyLookupUnavailable as error:
        # Refusing is the safe half of the choice. Sending the command as typed
        # would run it against the keyspace every reader shares, writing outside
        # this session and overwriting whatever is already there.
        LOGGER.error("refusing %s, key lookup is down: %s", argv[0], error)
        return {"error": True, "value": "ERR sandbox is unavailable, please retry"}

    session.connection.send_command(outgoing)
    reply = session.connection.read_reply()
    if namespace:
        reply = _replies.filter(argv, reply, namespace)

    if isinstance(reply, RespError):
        return {"error": True, "value": _readable(str(reply), namespace)}
    if isinstance(reply, RespStatus):
        return {"error": False, "value": str(reply), "status": True}
    return {"error": False, "value": encode_value(reply)}


def _readable(message: str, namespace: Namespace | None) -> str:
    """Keep the namespace out of error text the reader sees.

    Redis quotes the key or index it was given, so an error about `product:1`
    would otherwise come back naming `<session-uuid>:product:1` and read as a
    proxy bug rather than a typo.
    """
    if namespace is None:
        return message
    return message.replace(namespace.prefix, "")


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
        return jsonify({"replies": _all_failed(commands), "id": session_id or ""})
    except RedisAuthError as error:
        LOGGER.error("redis rejected the sandbox user %r: %s", config.REDIS_USERNAME, error)
        return jsonify({"replies": _all_failed(commands), "id": session_id or ""})

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


def _all_failed(commands: list) -> list[dict]:
    return [{"error": True, "value": "could not connect to redis"} for _ in commands]


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config.PORT)
