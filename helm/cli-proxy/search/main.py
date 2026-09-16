"""The endpoint search-modal.html already calls.

One route. The modal builds the URL itself from config.toml's `searchService`
and renders whatever JSON comes back, so part of this is not negotiable: the
parameter names, the two response keys, and the five fields of a result are
what that partial reads. See query.py for what each parameter does, measured
against the live service.

What is negotiable is everything the modal does not read, and that is what
makes this endpoint usable by anything else — a script, an agent, another
service. `limit` and `offset` page through a result set the modal only ever
sees the top of; four more fields per result say what a result actually is;
and a service that cannot reach its index now answers 503 rather than
pretending the corpus has nothing to say.

The index is built by indexer.py before this app starts, so a request never
waits on indexing and a failed index never becomes an endpoint that answers
nothing.
"""

import logging
import threading

from flask import Flask, jsonify, request

from resp import RespConnection, RespError, RespProtocolError
from search import config, query

logging.basicConfig(
    level=config.LOG_LEVEL,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
LOGGER = logging.getLogger("docs_search")

EMPTY_RESPONSE = {"total": 0, "results": []}


class ThreadConnection:
    """One Redis connection per worker thread, reopened when it breaks.

    A connection per request would open a socket for every keystroke -- the
    modal sends one request per character typed, with no debounce. Threads are
    long-lived under gunicorn's gthread worker, so the socket is kept and only
    replaced when the connection actually fails.
    """

    def __init__(self) -> None:
        self._local = threading.local()

    def get(self) -> RespConnection:
        connection = getattr(self._local, "connection", None)
        if connection is None:
            connection = RespConnection(
                config.REDIS_HOST, config.REDIS_PORT, config.SOCKET_TIMEOUT
            )
            self._local.connection = connection
        return connection

    def discard(self) -> None:
        connection = getattr(self._local, "connection", None)
        if connection is not None:
            connection.close()
            self._local.connection = None


CONNECTIONS = ThreadConnection()


def run_search(raw_query: str, product: str, limit: int, offset: int) -> tuple[dict, int]:
    """Return the response body and HTTP status for one search.

    An empty result list is an answer; a service that cannot reach its index is
    not, and the two used to be indistinguishable. A caller that only draws
    rows sees "no results" either way, but one deciding whether to trust the
    answer -- or an operator reading a log -- needs the difference.
    """
    built = query.build_query(raw_query, product)
    if not built:
        return dict(EMPTY_RESPONSE), 200
    command = query.search_command(config.INDEX_NAME, built, limit, offset)
    try:
        connection = CONNECTIONS.get()
        connection.send_command(command)
        reply = connection.read_reply()
    except (OSError, RespProtocolError) as error:
        LOGGER.error("search connection failed: %s", error)
        CONNECTIONS.discard()
        return {**EMPTY_RESPONSE, "error": "search unavailable"}, 503
    if isinstance(reply, RespError):
        # A query the parser rejects is a dead end for this keystroke, not for
        # the service: the modal renders "No results" and the next character
        # the reader types is very often valid again. So it stays a 200 with an
        # answer of nothing, and says why in the body rather than in the status.
        LOGGER.warning("search rejected for %r: %s", built, reply)
        return {**EMPTY_RESPONSE, "error": "query rejected"}, 200
    total, documents = query.parse_reply(reply)
    return {"total": total, "results": query.one_per_row(query.to_results(documents))}, 200


def bounded_int(raw: str | None, default: int, lowest: int, highest: int) -> int:
    """Read a query-string number, falling back to `default` and clamped to the range.

    A bad number is not worth a failed search: the modal never sends these at
    all, and a caller that sends limit=banana is better served by the default
    page than by an error it then has to handle.
    """
    try:
        value = int(raw)
    except (TypeError, ValueError):
        return default
    return max(lowest, min(highest, value))


app = Flask(__name__)


@app.get("/search")
def search():
    # `site` is read and dropped on purpose: the modal always sends it, and the
    # live service returns identical results with and without it.
    #
    # `limit` and `offset` are for everyone else. The modal sends neither and
    # gets the page size it has always had; a script reading more than the
    # first page has no other way through, since the reply carries the total
    # but only ever a page of it.
    body, status = run_search(
        request.args.get("q", ""),
        request.args.get("p", ""),
        bounded_int(request.args.get("limit"), config.RESULT_LIMIT, 1, config.MAX_RESULT_LIMIT),
        bounded_int(request.args.get("offset"), 0, 0, config.MAX_OFFSET),
    )
    return jsonify(body), status


@app.get("/healthz")
def healthz():
    """Readiness: the index has to exist before this pod takes traffic."""
    try:
        connection = CONNECTIONS.get()
        connection.send_command(["FT.INFO", config.INDEX_NAME])
        reply = connection.read_reply()
    except (OSError, RespProtocolError) as error:
        CONNECTIONS.discard()
        return jsonify({"status": "unavailable", "detail": str(error)}), 503
    if isinstance(reply, RespError):
        return jsonify({"status": "no index", "detail": str(reply)}), 503
    return jsonify({"status": "ok"})
