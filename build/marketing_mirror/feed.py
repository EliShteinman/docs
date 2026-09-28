"""The mirror's search feed, mirror.ndjson, built from the pages' Markdown.

One record per page, in the shape the documentation's own feed uses
(layouts/_default/single.json), because the search service reads both with the
same code. A page redis.io publishes no Markdown for -- a listing, an author
page -- has no body worth indexing and gets no record.
"""

from __future__ import annotations

import html
import json
import re
from collections.abc import Iterator
from pathlib import Path

from build.marketing_mirror import settings

SCHEMA_VERSION = "2"

_TITLE = re.compile(r"^#\s+(.+)$", re.MULTILINE)
_DESCRIPTION = re.compile(r'<meta\s+name="description"\s+content="([^"]*)"')
_FIELD = r"\*\*{name}:\*\*\s*([^|\n]+)"
_UPDATED = re.compile(_FIELD.format(name="Updated"))
_PUBLISHED = re.compile(_FIELD.format(name="Published"))
_CATEGORIES = re.compile(_FIELD.format(name="Categories"))


def _first(pattern: re.Pattern[str], text: str) -> str:
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def record(path: str, markdown: str, page_html: str) -> dict[str, object]:
    categories = _first(_CATEGORIES, markdown)
    return {
        "schema_version": SCHEMA_VERSION,
        "id": path.strip("/"),
        "title": _first(_TITLE, markdown),
        "url": path,
        "summary": html.unescape(_first(_DESCRIPTION, page_html)),
        "content": markdown,
        "tags": [tag.strip() for tag in categories.split(",") if tag.strip()],
        "last_updated": _first(_UPDATED, markdown) or _first(_PUBLISHED, markdown),
    }


def records(site_dir: Path) -> Iterator[dict[str, object]]:
    for markdown_path in sorted(site_dir.rglob("*.md")):
        relative = markdown_path.relative_to(site_dir).with_suffix("")
        path = f"/{relative.as_posix()}/"
        page = site_dir / relative / "index.html"
        if not page.is_file():
            continue
        yield record(
            path,
            markdown_path.read_text(encoding="utf-8"),
            page.read_text(encoding="utf-8"),
        )


def write_feed(site_dir: Path) -> int:
    """Write mirror.ndjson at the root of the site. Returns the record count."""
    lines = [json.dumps(entry, ensure_ascii=False) for entry in records(site_dir)]
    (site_dir / settings.FEED_NAME).write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    return len(lines)
