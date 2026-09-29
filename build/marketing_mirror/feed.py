"""The mirror's search feed, mirror.ndjson.

One record per page, in the shape the documentation's own feed uses
(layouts/_default/single.json, then build/transform_json_sections.ts), because
the search service reads both with the same code -- and it indexes a page's
`sections`, not its `content`.

A page's text is its Markdown where redis.io publishes one, and its rendered
HTML where it does not (page_text.py). Listings -- a section's index, a blog
category or author page -- carry no text of their own and get no record.
"""

from __future__ import annotations

import html
import json
import re
from collections.abc import Iterator
from pathlib import Path

from build.marketing_mirror import page_text, settings

SCHEMA_VERSION = "2"

_TITLE = re.compile(r"^#\s+(.+)$", re.MULTILINE)
_DESCRIPTION = re.compile(r'<meta\s+name="description"\s+content="([^"]*)"')
_FIELD = r"\*\*{name}:\*\*\s*([^|\n]+)"
_UPDATED = re.compile(_FIELD.format(name="Updated"))
_PUBLISHED = re.compile(_FIELD.format(name="Published"))
_CATEGORIES = re.compile(_FIELD.format(name="Categories"))
_CODE_BLOCK = re.compile(r"```[^\n]*\n.*?```", re.DOTALL)
_SECTION_HEADING = re.compile(r"^#{2,3}\s+(.+)$", re.MULTILINE)
_SLUG_DROP = re.compile(r"[^\w\s-]")
_SLUG_SPACE = re.compile(r"\s+")


def _first(pattern: re.Pattern[str], text: str) -> str:
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def _slug(title: str) -> str:
    return _SLUG_SPACE.sub("-", _SLUG_DROP.sub("", title.lower()).strip())


def sections(markdown: str) -> list[dict[str, str]]:
    """The page's prose split at its ## and ### headings, code left out.

    Code is replaced with the placeholder the documentation's feed uses, which
    the search service knows to skip.
    """
    prose = _CODE_BLOCK.sub("[code example]", markdown)
    headings = list(_SECTION_HEADING.finditer(prose))
    starts = [heading.start() for heading in headings] + [len(prose)]
    found: list[dict[str, str]] = []
    intro = prose[: starts[0]].strip()
    if intro:
        found.append(
            {"id": "overview", "title": "Overview", "role": "overview", "text": intro}
        )
    for heading, end in zip(headings, starts[1:]):
        title = heading.group(1).strip()
        text = prose[heading.end() : end].strip()
        found.append(
            {"id": _slug(title), "title": title, "role": "content", "text": text}
        )
    return found


def record(path: str, markdown: str, page_html: str) -> dict[str, object]:
    categories = _first(_CATEGORIES, markdown)
    return {
        "schema_version": SCHEMA_VERSION,
        "id": path.strip("/"),
        "title": _first(_TITLE, markdown),
        "url": path,
        "summary": html.unescape(_first(_DESCRIPTION, page_html)),
        "content": markdown,
        "sections": sections(markdown),
        "tags": [tag.strip() for tag in categories.split(",") if tag.strip()],
        "last_updated": _first(_UPDATED, markdown) or _first(_PUBLISHED, markdown),
    }


def is_listing(path: str) -> bool:
    if path in settings.SECTIONS:
        return True
    return path.startswith(("/blog/category/", "/blog/author/"))


def html_record(path: str, page_html: str, lastmod: str) -> dict[str, object]:
    text = page_text.content(page_html)
    entry = record(path, text, page_html)
    entry["title"] = page_text.title(page_html)
    entry["last_updated"] = lastmod
    return entry


def records(site_dir: Path, dates: dict[str, str]) -> Iterator[dict[str, object]]:
    for page in sorted(site_dir.rglob("index.html")):
        relative = page.parent.relative_to(site_dir)
        path = f"/{relative.as_posix()}/"
        if relative == Path(".") or is_listing(path):
            continue
        page_html = page.read_text(encoding="utf-8")
        markdown = site_dir / f"{relative.as_posix()}.md"
        if markdown.is_file():
            entry = record(path, markdown.read_text(encoding="utf-8"), page_html)
            entry["last_updated"] = entry["last_updated"] or dates.get(path, "")
            yield entry
        elif page_text.content(page_html):
            yield html_record(path, page_html, dates.get(path, ""))


def write_feed(site_dir: Path, dates: dict[str, str]) -> int:
    """Write mirror.ndjson at the root of the site. Returns the record count."""
    lines = [
        json.dumps(entry, ensure_ascii=False) for entry in records(site_dir, dates)
    ]
    (site_dir / settings.FEED_NAME).write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    return len(lines)
