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

# The mirrored sections ship as an image of their own, and the pages they carry
# left the documentation's feed with them (build/split_mirror.py). Empty when
# the mirror is not deployed, which is what keeps search from answering with a
# blog post this site does not serve.
MIRROR_FEED_PATH = os.environ.get("SEARCH_MIRROR_FEED", "")

# redis.io returns at most 30 hits and reports the full match count separately.
# The modal renders every hit it is handed, so this is what stops a broad query
# from painting thousands of rows.
RESULT_LIMIT = int(os.environ.get("SEARCH_RESULT_LIMIT", "30"))

# A caller that is not the modal -- a script or an agent -- may ask for another
# page size with `limit`, up to this. Capped because the whole reply is built in
# memory and this endpoint is reachable by anyone who can reach the site.
MAX_RESULT_LIMIT = int(os.environ.get("SEARCH_MAX_RESULT_LIMIT", "100"))

# How far `offset` may page. The query engine walks the whole result set up to
# the offset on every request, so deep paging costs more the further it goes.
MAX_OFFSET = int(os.environ.get("SEARCH_MAX_OFFSET", "1000"))

# hierarchy[0] on every result. redis.io sends the docs home page's heading,
# which is not the Hugo site title ("Docs" in config.toml) and so cannot be
# derived from the feed -- it is carried here instead.
ROOT_CRUMB = os.environ.get("SEARCH_ROOT_CRUMB", "Welcome to Redis Docs")

# Documents per pipelined flush while indexing. Large enough that 5,679 pages
# are not 5,679 round trips, small enough not to hold the whole feed in a
# single write buffer.
INDEX_BATCH = int(os.environ.get("SEARCH_INDEX_BATCH", "500"))

# How much of its relevance a page from a numbered documentation version keeps.
# Numbered, not older: the current documentation is the tree with no version in
# its path, tagged `latest` by build/tag_ndjson_versions.py, and every numbered
# tree is an archive of it -- so 8.0 is weighted down exactly like 7.4. `latest`
# is a real release and not a synonym for the newest number: Redis Software's
# numbered trees stop at 8.0, while 8.2 publishes only in the unversioned tree.
# Which release it is is nowhere in machine-readable form, so a result says
# `latest` rather than the number.
# The docs publish the same page once per version -- 45% of the index is
# versioned copies -- and without this the copies crowd out the current page:
# measured on a real build, "rack zone awareness" answered with version 7.22
# first, and "database*" returned 27 versioned pages in a top 30.
#
# A multiplier rather than a filter, because the old pages are still worth
# finding: a reader on 7.4 searching for something that only exists in 7.4
# still gets it, just below the current page when both match equally.
#
# This is the floor: what the OLDEST version tree of a product keeps.
VERSION_WEIGHT = float(os.environ.get("SEARCH_VERSION_WEIGHT", "0.3"))

# What the newest version tree keeps, with the trees in between spread evenly
# from the floor up to it. The archive has an order of its own -- 8.0 is a
# better answer than 7.4, which is a better answer than 7.22 -- and one weight
# for all of them threw that away.
#
# Below 1 on purpose, so the current documentation still outranks the newest
# archived copy of the same page.
VERSION_NEWEST_WEIGHT = float(os.environ.get("SEARCH_VERSION_NEWEST_WEIGHT", "0.6"))

# The bonus a page gets for carrying the typed words, whole, in its title. See
# query.py for why a prefix alone ranks a command's own page below the long
# reference pages that list it. 5 was measured on the real index.
TITLE_BOOST = float(os.environ.get("SEARCH_TITLE_BOOST", "5"))

# The version tag the docs build gives a page that is not in a version tree
# (build/tag_ndjson_versions.py).
CURRENT_VERSION = os.environ.get("SEARCH_CURRENT_VERSION", "latest")

LOG_LEVEL = os.environ.get("SEARCH_LOG_LEVEL", "INFO").upper()
