"""Reading the blog out of the Sanity dataset behind redis.io.

The dataset is public, so this needs no credentials. Documents come back whole
via GROQ; the only shaping done here is dereferencing authors and categories,
which are stored as references and would otherwise arrive as opaque ids.

An author document has no `name`: it carries `firstName`, `lastName` and
`role`, so the three are projected and joined on this side. Asking for `name`
returns null for every post, which is quiet enough to ship a mirror with no
bylines at all.

Paged rather than fetched in one request: the API caps a response, and 1,100
posts of Portable Text is more than one response can carry.
"""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
from collections.abc import Iterator

PROJECT_ID = "sy1jschh"
DATASET = "production"
API_VERSION = "v2021-10-21"
# The CDN host, not the live API: this content changes a few times a week and
# an edge-cached read is what every visitor to redis.io already gets.
API_HOST = f"https://{PROJECT_ID}.apicdn.sanity.io"

DOCUMENT_TYPE = "blogPost"
PAGE_SIZE = 40

# Ordered by _id rather than by date, so paging cannot skip or repeat a
# document when two posts share a publish date.
_QUERY = (
    '*[_type=="{doc_type}"]|order(_id)[{start}...{end}]'
    "{{_id,_updatedAt,title,tagline,publishDate,"
    '"slug":slug.current,content,image,'
    '"authors":author[]->{{firstName,lastName,role}},'
    '"categories":categories[]->title}}'
)

# Pages are a different document type with a different shape: no publish date,
# no author, and their prose spread across a list of layout sections rather
# than one Portable Text field. pages.py reads that shape.
PAGE_TYPE = "page"

_PAGE_QUERY = (
    '*[_type=="{doc_type}" && pathname match "{prefix}"]|order(pathname)'
    "[{start}...{end}]"
    '{{_id,_updatedAt,_createdAt,title,pathname,sections}}'
)

USER_AGENT = "redis-docs-airgap-site-mirror/1.0"


class SanityError(RuntimeError):
    """The dataset could not be read."""


def _get(url: str, timeout: float) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise SanityError(f"reading {url} failed: {error}") from error


def query_url(query: str) -> str:
    path = f"{API_HOST}/{API_VERSION}/data/query/{DATASET}"
    return path + "?" + urllib.parse.urlencode({"query": query})


def count_posts(timeout: float = 60.0) -> int:
    """Return how many posts the dataset holds."""
    result = _get(query_url(f'count(*[_type=="{DOCUMENT_TYPE}"])'), timeout)
    return int(result.get("result") or 0)


def fetch_posts(timeout: float = 60.0, page_size: int = PAGE_SIZE) -> Iterator[dict]:
    """Yield every blog post document, a page at a time."""
    start = 0
    while True:
        query = _QUERY.format(doc_type=DOCUMENT_TYPE, start=start, end=start + page_size)
        page = _get(query_url(query), timeout).get("result") or []
        if not page:
            return
        yield from page
        start += page_size


def count_pages(prefix: str, timeout: float = 60.0) -> int:
    """Return how many page documents live under a pathname prefix."""
    query = f'count(*[_type=="{PAGE_TYPE}" && pathname match "{prefix}"])'
    return int(_get(query_url(query), timeout).get("result") or 0)


def fetch_pages(
    prefix: str, timeout: float = 60.0, page_size: int = PAGE_SIZE
) -> Iterator[dict]:
    """Yield every page document under a pathname prefix, a page at a time."""
    start = 0
    while True:
        query = _PAGE_QUERY.format(
            doc_type=PAGE_TYPE, prefix=prefix, start=start, end=start + page_size
        )
        batch = _get(query_url(query), timeout).get("result") or []
        if not batch:
            return
        yield from batch
        start += page_size
