"""Building the search index in Redis from the docs feed.

Run as a program before the web app starts, not from inside it: indexing that
fails should stop the container with a message rather than leave a served
endpoint answering nothing, and readiness then follows the process rather than
having to be inferred.

Redis 8 carries the query engine in the base image the chart already deploys
(redis:8.10.0-alpine), so this adds no image and no dependency -- the commands
go out over resp.py, the RESP implementation the CLI proxy already ships.
"""

import logging
import sys

from resp import RespConnection, RespError
from search import config
from search.hierarchy import BreadcrumbIndex
from search.sources import BLOG_SOURCE, Document, load_documents
import json

LOGGER = logging.getLogger("docs_search.indexer")

# WEIGHT puts a hit in the page title above the same word buried in its body,
# and the breadcrumb between them: a page called "Vector search" should beat a
# page that mentions vector search once, which is what the live ordering does.
_SCHEMA = [
    "title", "TEXT", "WEIGHT", "5",
    "crumbs", "TEXT", "WEIGHT", "2",
    "body", "TEXT", "WEIGHT", "1",
    "product", "TAG",
    "version", "TAG",
    "source", "TAG",
]


class IndexingError(RuntimeError):
    """Redis refused a command the index cannot be built without."""


# "there is no index to drop" is the normal state of a first run, and Redis has
# worded it more than one way: 8.x answers "SEARCH_INDEX_NOT_FOUND Index not
# found: docs", earlier builds "Unknown index name". Both are matched, because
# treating either as fatal would mean the pod never indexes on a clean Redis.
_NO_SUCH_INDEX = ("index not found", "unknown index")


def _is_missing_index(reply: RespError) -> bool:
    text = str(reply).lower()
    return any(marker in text for marker in _NO_SUCH_INDEX)


def _run(connection: RespConnection, argv: list[str], tolerate_missing_index: bool = False) -> object:
    connection.send_command(argv)
    reply = connection.read_reply()
    if isinstance(reply, RespError):
        if tolerate_missing_index and _is_missing_index(reply):
            return reply
        raise IndexingError(f"{argv[0]} failed: {reply}")
    return reply


def allow_single_character_prefixes(connection: RespConnection) -> None:
    """Let a one-letter prefix match, the way the live service does.

    The modal fires a request on the very first keystroke, and redis.io answers
    `v*` with 316 hits. The query engine's default minimum prefix is two
    characters, which would answer the first keystroke of every search with
    "No results" and only start working on the second.
    """
    _run(connection, ["FT.CONFIG", "SET", "MINPREFIX", "1"])


def create_index(connection: RespConnection, index: str, key_prefix: str) -> None:
    """Drop any previous index and create a fresh one.

    Dropped rather than reused because the pod indexes on every start: a
    surviving index from an older image would keep documents whose pages no
    longer exist, and a schema change would silently not apply. DD also clears
    the documents, so the keyspace does not accumulate.
    """
    _run(connection, ["FT.DROPINDEX", index, "DD"], tolerate_missing_index=True)
    _run(
        connection,
        [
            "FT.CREATE", index, "ON", "HASH", "PREFIX", "1", key_prefix,
            # Multiplies each document's relevance, so a current page outranks
            # the same page from an older version. See config.VERSION_WEIGHT.
            "SCORE_FIELD", "docscore",
            "SCHEMA", *_SCHEMA,
        ],
    )
    LOGGER.info("created index %s over prefix %s", index, key_prefix)


def document_score(version: str) -> str:
    """Return the relevance multiplier for a page of this documentation version."""
    return "1" if not version or version == config.CURRENT_VERSION else str(config.VERSION_WEIGHT)


def _document_fields(document: Document, crumbs: list[str]) -> list[str]:
    return [
        "docscore", document_score(document.version),
        "title", document.title,
        "crumbs", " ".join(crumbs),
        "body", document.body,
        "product", document.product,
        "version", document.version,
        "source", document.source,
        "url", document.url,
        "hierarchy", json.dumps(crumbs, ensure_ascii=False),
    ]


def index_documents(
    connection: RespConnection,
    documents: list[Document],
    breadcrumbs: BreadcrumbIndex,
    key_prefix: str,
    batch_size: int,
) -> int:
    """Write every document into Redis, pipelining `batch_size` at a time."""
    written = 0
    for start in range(0, len(documents), batch_size):
        batch = documents[start : start + batch_size]
        for document in batch:
            # The blog heads its own group rather than sitting under the docs
            # root crumb: its trail already starts with the section's own title.
            root = "" if document.source == BLOG_SOURCE else None
            crumbs = breadcrumbs.crumbs_for(document.doc_id, root)
            fields = _document_fields(document, crumbs)
            connection.send_command(["HSET", key_prefix + document.doc_id, *fields])
        for document in batch:
            reply = connection.read_reply()
            if isinstance(reply, RespError):
                raise IndexingError(f"HSET failed for {document.url}: {reply}")
        written += len(batch)
        LOGGER.debug("indexed %d/%d documents", written, len(documents))
    return written


def build_index() -> int:
    """Load the feed and rebuild the whole index. Returns the document count."""
    documents = load_documents(config.DOCS_FEED_PATH)
    if not documents:
        raise IndexingError(f"no documents found in {config.DOCS_FEED_PATH}")
    breadcrumbs = BreadcrumbIndex.from_documents(config.ROOT_CRUMB, documents)
    connection = RespConnection(config.REDIS_HOST, config.REDIS_PORT, config.SOCKET_TIMEOUT)
    try:
        allow_single_character_prefixes(connection)
        create_index(connection, config.INDEX_NAME, config.KEY_PREFIX)
        written = index_documents(
            connection, documents, breadcrumbs, config.KEY_PREFIX, config.INDEX_BATCH
        )
    finally:
        connection.close()
    LOGGER.info("indexed %d documents into %s", written, config.INDEX_NAME)
    return written


def main() -> int:
    logging.basicConfig(
        level=config.LOG_LEVEL,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    try:
        build_index()
    except (IndexingError, OSError) as error:
        LOGGER.critical("indexing failed: %s", error)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
