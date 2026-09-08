"""The endpoint search-modal.html already calls.

One route. The modal builds the URL itself from config.toml's `searchService`
and renders whatever JSON comes back, so nothing here is negotiable: the
parameter names, the two response keys, and the five fields of a result are
what that partial reads. See query.py for what each parameter does, measured
against the live service.

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


def run_search(raw_query: str, product: str) -> dict:
    """Return the response body for one search, or the empty body on any failure."""
    built = query.build_query(raw_query, product)
    if not built:
        return EMPTY_RESPONSE
    command = query.search_command(config.INDEX_NAME, built, config.RESULT_LIMIT)
    try:
        connection = CONNECTIONS.get()
        connection.send_command(command)
        reply = connection.read_reply()
    except (OSError, RespProtocolError) as error:
        LOGGER.error("search connection failed: %s", error)
        CONNECTIONS.discard()
        return EMPTY_RESPONSE
    if isinstance(reply, RespError):
        # A query the parser rejects is a dead end for this keystroke, not for
        # the service: the modal renders "No results" and the next character
        # the reader types is very often valid again.
        LOGGER.warning("search rejected for %r: %s", built, reply)
        return EMPTY_RESPONSE
    total, documents = query.parse_reply(reply)
    return {"total": total, "results": query.to_results(documents)}


app = Flask(__name__)


@app.get("/search")
def search():
    # `site` is read and dropped on purpose: the modal always sends it, and the
    # live service returns identical results with and without it.
    return jsonify(
        run_search(request.args.get("q", ""), request.args.get("p", ""))
    )


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
