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
import uuid

from flask import Flask, jsonify, request

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
LOGGER = logging.getLogger("cli_proxy")

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))
SOCKET_TIMEOUT = float(os.environ.get("REDIS_TIMEOUT", "5"))

# Integers beyond this magnitude lose precision once serialized as JSON numbers
# and parsed by the browser, so they are tagged {"$int": "<decimal>"} instead.
JS_MAX_SAFE_INTEGER = 2**53 - 1

CRLF = b"\r\n"


class RespProtocolError(Exception):
    """The server sent bytes that do not conform to the RESP grammar."""


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


class Session:
    """A Redis connection plus a lock that serializes the worker threads sharing it."""

    def __init__(self, connection: RespConnection) -> None:
        self.connection = connection
        self.lock = threading.Lock()


_sessions: dict[str, Session] = {}
_sessions_lock = threading.Lock()


def get_session(session_id: str | None) -> tuple[Session, str]:
    sid = session_id or str(uuid.uuid4())

    with _sessions_lock:
        session = _sessions.get(sid)
    if session is not None:
        return session, sid

    # Connect outside the global lock so a slow/unreachable Redis never stalls
    # every other worker thread.
    connection = RespConnection(REDIS_HOST, REDIS_PORT, SOCKET_TIMEOUT)
    with _sessions_lock:
        existing = _sessions.get(sid)
        if existing is not None:
            connection.close()
            return existing, sid
        session = Session(connection)
        _sessions[sid] = session
    LOGGER.info("opened redis session %s", sid)
    return session, sid


def drop_session(sid: str) -> None:
    with _sessions_lock:
        session = _sessions.pop(sid, None)
    if session is not None:
        session.connection.close()
        LOGGER.warning("dropped redis session %s", sid)


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

    try:
        session, sid = get_session(session_id)
    except OSError as error:
        LOGGER.error("could not reach redis: %s", error)
        replies = [{"error": True, "value": "could not connect to redis"} for _ in commands]
        return jsonify({"replies": replies, "id": session_id or ""})

    replies: list[dict] = []
    with session.lock:
        for index, command in enumerate(commands):
            try:
                replies.append(run_command(session, command))
            except (OSError, RespProtocolError) as error:
                LOGGER.error("redis failure on session %s: %s", sid, error)
                drop_session(sid)
                replies.extend(
                    {"error": True, "value": "redis connection lost, please retry"}
                    for _ in commands[index:]
                )
                break

    return jsonify({"replies": replies, "id": sid})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8090")))