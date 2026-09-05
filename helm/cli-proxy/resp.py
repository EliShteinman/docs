"""RESP wire handling for the CLI proxy.

Replies are parsed straight off the socket because high-level clients collapse
the simple/bulk-string distinction into a plain string, and the widget needs
that distinction to render output byte-for-byte like the native redis-cli:

  * simple-string replies (+OK, +PONG)  -> {"value": "OK", "status": true}  (no quotes)
  * bulk-string replies   ($...)        -> {"value": "<text>"}              (quoted)
  * integer replies       (:...)        -> {"value": 42} or {"value": {"$int": "..."}}
  * error replies         (-ERR ...)    -> {"error": true, "value": "<msg>"}

RESP3 replies (after HELLO 3) are mapped back onto these RESP2-shaped values.
"""

import logging
import socket

LOGGER = logging.getLogger("cli_proxy.resp")

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


