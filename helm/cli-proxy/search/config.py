"""Every knob the search service reads from its environment, in one place.

Plain os.environ, for the reason the CLI proxy's own config.py gives one
directory up: this ships inside that same image, whose dependencies are flask
and gunicorn and nothing else, and a settings library is another wheel in the
air-gapped bundle for the sake of a dozen scalars.
"""

import os

REDIS_HOST = os.environ.get("SEARCH_REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("SEARCH_REDIS_PORT", "6379"))
SOCKET_TIMEOUT = float(os.environ.get("SEARCH_REDIS_TIMEOUT", "10"))

INDEX_NAME = os.environ.get("SEARCH_INDEX_NAME", "docs")
KEY_PREFIX = os.environ.get("SEARCH_KEY_PREFIX", "doc:")

# The RAG feed the docs build already produces (build/generate_ndjson.py), one
# JSON record per page. An init container copies it out of the docs image into
# the volume this points at.
DOCS_FEED_PATH = os.environ.get("SEARCH_DOCS_FEED", "/corpus/docs.ndjson")

# redis.io returns at most 30 hits and reports the full match count separately.
# The modal renders every hit it is handed, so this is what stops a broad query
# from painting thousands of rows.
RESULT_LIMIT = int(os.environ.get("SEARCH_RESULT_LIMIT", "30"))

# hierarchy[0] on every result. redis.io sends the docs home page's heading,
# which is not the Hugo site title ("Docs" in config.toml) and so cannot be
# derived from the feed -- it is carried here instead.
ROOT_CRUMB = os.environ.get("SEARCH_ROOT_CRUMB", "Welcome to Redis Docs")

# Documents per pipelined flush while indexing. Large enough that 5,679 pages
# are not 5,679 round trips, small enough not to hold the whole feed in a
# single write buffer.
INDEX_BATCH = int(os.environ.get("SEARCH_INDEX_BATCH", "500"))

LOG_LEVEL = os.environ.get("SEARCH_LOG_LEVEL", "INFO").upper()
