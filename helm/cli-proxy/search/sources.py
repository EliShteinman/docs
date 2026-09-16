"""Where the searchable documents come from.

Today there is one source: docs.ndjson, the RAG feed the docs build already
produces (build/generate_ndjson.py, run by both airgap-multibuild.sh and
airgap-build.yml). The feed is read rather than the per-page index.json files
because that script already dropped what must not be indexed -- redirect
tombstones -- so the filtering does not get reimplemented here.

The mirrored blog arrives through the same feed rather than a second one: its
posts are Hugo pages like any other, so the build already writes them into
docs.ndjson. What tells them apart is where they live on the site, which is
what `source` records.
"""

import json
import logging
import re
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

from search.paths import to_href, to_path
from search.product import product_of

LOGGER = logging.getLogger("docs_search.sources")

DOCS_SOURCE = "docs"
BLOG_SOURCE = "blog"
SITE_SOURCE = "site"

# The section the mirrored blog is published under (build/site_mirror).
BLOG_PREFIX = "/blog/"

# The other sections build/site_mirror publishes. They are kept apart from the
# documentation because a result's first crumb is the heading the modal files
# it under, and filing a customer story or a product comparison under "Welcome
# to Redis Docs" tells a reader it is documentation.
#
# The glossary is deliberately absent. Its terms publish at /glossary/<term>/,
# inside the documentation's own glossary section, so the documentation's
# heading is the right one for them.
MIRRORED_PREFIXES = (
    "/tutorials/",
    "/technology/",
    "/compare/",
    "/solutions/",
    "/customers/",
    "/resources/architecture-diagrams/",
)

# The feed keeps its links as markdown, and their targets carry the
# __DOCS_BASE_URL__ placeholder that nginx substitutes at response time
# (configmap.yaml). The indexer reads the file, not the HTTP response, so it
# would index the placeholder as a term and let a reader searching for "docs"
# match every link on the site. Link text is worth indexing; link targets are
# not, so the target is dropped and the text kept.
_MARKDOWN_LINK = re.compile(r"!?\[([^\]]*)\]\([^)]*\)")
# What the feed leaves where a fenced code block was -- 35,351 of them in a real
# build. Indexed, they would make "code" and "example" match nearly every page.
_CODE_PLACEHOLDER = re.compile(r"\[code example\]")
_MARKDOWN_NOISE = re.compile(r"[`*>#|]+")
# An underscore is emphasis only at the edge of a word. Inside one it is part
# of a name -- `eviction_policy`, `maxmemory_policy` -- which the index keeps as
# a single term, and splitting it here would leave the page that documents the
# key unfindable by the key's own name.
_EMPHASIS_UNDERSCORE = re.compile(r"(?<!\w)_+|_+(?!\w)")
_WHITESPACE = re.compile(r"\s+")


@dataclass(frozen=True)
class Document:
    """One indexable page, in the shape the index and the response both need."""

    # The normalized path: the Redis key, and what breadcrumb lookup joins on.
    doc_id: str
    title: str
    # What a result links to, keeping the trailing slash so a click does not
    # cost a redirect.
    url: str
    body: str
    version: str
    product: str
    source: str


def clean_body(content: str) -> str:
    """Strip markdown scaffolding from `content` so only prose is indexed."""
    without_code = _CODE_PLACEHOLDER.sub(" ", content)
    without_links = _MARKDOWN_LINK.sub(r"\1", without_code)
    without_noise = _MARKDOWN_NOISE.sub(" ", without_links)
    without_emphasis = _EMPHASIS_UNDERSCORE.sub(" ", without_noise)
    return _WHITESPACE.sub(" ", without_emphasis).strip()


def page_text(record: dict) -> str:
    """Return the prose of a feed record: its summary, then every section.

    The feed has no whole-page text field. A page's prose is `sections`, one
    entry per heading, so reading anything else indexes the one-line summary
    and nothing a reader would search the body for.
    """
    parts = [record.get("summary") or ""]
    for section in record.get("sections") or []:
        if isinstance(section, dict):
            parts.append(section.get("title") or "")
            parts.append(section.get("text") or "")
    return " ".join(part for part in parts if part)


def _under(path: str, prefix: str) -> bool:
    """Whether `path` is `prefix` itself or a page inside it.

    `to_path` drops the trailing slash, so a section's own index arrives as
    "/blog" and never matches a "/blog/" prefix test on its own.
    """
    return path == prefix.rstrip("/") or path.startswith(prefix)


def source_of(path: str) -> str:
    """Return which body of content a page belongs to, from where it is published.

    The mirrored sections share the feed with the documentation, so a reader
    who wants one and not the other needs them distinguishable at query time --
    and the indexer needs to know which pages are not documentation before it
    can give them a heading of their own.
    """
    if _under(path, BLOG_PREFIX):
        return BLOG_SOURCE
    if any(_under(path, prefix) for prefix in MIRRORED_PREFIXES):
        return SITE_SOURCE
    return DOCS_SOURCE


def read_feed(path: Path | str) -> Iterator[dict]:
    """Yield each parsed record of an NDJSON feed, skipping unreadable lines.

    A single malformed line must not cost the whole index: the site is more
    useful missing one page than missing search entirely.
    """
    with open(path, encoding="utf-8") as feed:
        for number, line in enumerate(feed, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                yield json.loads(stripped)
            except json.JSONDecodeError:
                LOGGER.warning("skipping malformed feed record at line %d", number)


def to_document(record: dict, source: str = "") -> Document | None:
    """Build a Document from a feed record, or None when the record cannot be used.

    `source` is derived from the page's own path unless the caller names one,
    which a future separate feed would.
    """
    url = record.get("url") or ""
    title = record.get("title") or ""
    if not url or not title:
        return None
    path = to_path(url)
    return Document(
        doc_id=path,
        title=title,
        url=to_href(url),
        body=clean_body(page_text(record)),
        # tag_ndjson_versions.py adds `version` to every record; a feed built
        # before that step simply has none, and the tag is left empty.
        version=record.get("version") or "",
        product=product_of(path),
        source=source or source_of(path),
    )


def load_documents(path: Path | str, source: str = "") -> list[Document]:
    """Read `path` and return every usable Document in it."""
    documents = [
        document
        for document in (to_document(record, source) for record in read_feed(path))
        if document is not None
    ]
    LOGGER.info("loaded %d documents from %s", len(documents), path)
    return documents
