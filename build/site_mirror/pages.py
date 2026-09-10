"""Rendering redis.io's page-builder pages as markdown.

The /technology/ tree is technical writing -- cluster architecture, durability,
geo-distribution -- but it is not stored the way the blog is. A blog post is one
Portable Text field; a page is a list of layout sections, each with its own
shape, and the prose is scattered across their `content`, `description` and
`cards` fields.

So this module is a section-by-section reader, not a general one: it covers the
nine section types the /technology/ pages actually use, checked against all
eleven of them. A section type it does not know contributes nothing, which is
the right failure -- a page loses a block rather than gaining a broken one.

What it deliberately drops is the furniture: the closing "Want to learn more?"
call-to-action and the related-resources carousel. Both are link lists pointing
at pages an air-gapped reader cannot open.
"""

from __future__ import annotations

import html
import re

from build.site_mirror.links import localize
from build.site_mirror.portable_text import ImageResolver, render

# Section titles arrive as HTML fragments -- "<h2>Benefits</h2>" -- because the
# page builder lets an editor choose the heading level inline.
_TAG = re.compile(r"<[^>]+>")

DROPPED_SECTIONS = frozenset({"closingCtaSection", "cardCarouselSection"})

# The section types whose own title is the page's hero title, already carried in
# the frontmatter. Repeating it as a heading gives every page a duplicate H1.
_HERO_SECTIONS = frozenset({"headerSimpleSection", "resourceHeaderSection"})


def strip_html(raw: object) -> str:
    """Return the plain text of a section title.

    A title is usually an HTML fragment, but not always: some sections in the
    /solutions/ tree carry Portable Text there instead, which is why this takes
    an object rather than a string. Anything it cannot read becomes empty, and
    the section loses its heading rather than the run losing the page.
    """
    if isinstance(raw, list):
        return " ".join(strip_html(item) for item in raw).strip()
    if isinstance(raw, dict):
        if raw.get("_type") == "span":
            return (raw.get("text") or "").strip()
        # Only containers are descended into. A block's scalar fields are
        # metadata -- `style`, `_key` -- and joining them in turns a heading
        # into "normal Fraud detection". Text lives in spans, handled above.
        return " ".join(
            strip_html(v) for v in raw.values() if isinstance(v, (list, dict))
        ).strip()
    if not isinstance(raw, str):
        return ""
    return html.unescape(_TAG.sub("", raw)).strip()


def _heading(raw: object, level: int) -> str:
    text = strip_html(raw)
    return f"{'#' * level} {text}" if text else ""


def _join(pieces: list[str]) -> str:
    return "\n\n".join(piece for piece in pieces if piece and piece.strip())


def _items(section: dict) -> list[dict]:
    """Return a section's repeated entries, whatever this section type calls them."""
    for key in ("cards", "items", "accordionItems"):
        entries = section.get(key)
        if isinstance(entries, list):
            return [entry for entry in entries if isinstance(entry, dict)]
    return []


def _item_body(item: dict, resolve_image: ImageResolver) -> str:
    """Return an entry's prose, from whichever field this section type used.

    A field that is present but empty is passed over rather than returned: a
    card carrying `content: []` and a real `description` would otherwise render
    as nothing, because the empty list is still a list.
    """
    for key in ("content", "description"):
        value = item.get(key)
        if isinstance(value, list):
            rendered = render(value, resolve_image)
            if rendered.strip():
                return rendered
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def _render_section(section: dict, resolve_image: ImageResolver, level: int) -> str:
    kind = section.get("_type")
    if kind in DROPPED_SECTIONS:
        return ""

    parts = []
    if kind not in _HERO_SECTIONS:
        parts.append(_heading(section.get("title") or "", level))

    content = section.get("content")
    if isinstance(content, list):
        parts.append(render(content, resolve_image))

    for item in _items(section):
        parts.append(_heading(item.get("title") or "", level + 1))
        parts.append(_item_body(item, resolve_image))

    # A section may lead with a video instead of prose. The player is off-site,
    # so it becomes a link, the same choice the blog renderer makes.
    video = section.get("videoUrl")
    if isinstance(video, str) and video.strip():
        # Through localize for the same reason the blog renderer sends its own
        # video URLs through it: some of them point back at redis.io/blog.
        target = localize(video.strip())
        if target:
            parts.append(f"[Watch the video]({target})")

    return _join(parts)


def render_page(page: dict, resolve_image: ImageResolver, level: int = 2) -> str:
    """Return the markdown for one page-builder page."""
    sections = page.get("sections") or []
    return _join(
        [
            _render_section(section, resolve_image, level)
            for section in sections
            if isinstance(section, dict)
        ]
    )


def section_types(page: dict) -> set[str]:
    """Return the section types a page uses. For reporting what went unrendered."""
    return {s.get("_type") for s in (page.get("sections") or []) if isinstance(s, dict)}


KNOWN_SECTIONS: frozenset[str] = frozenset(
    {
        "headerSimpleSection",
        "resourceHeaderSection",
        "richTextSection",
        "twoColDefaultSection",
        "cardGridSection",
        "grid2x2Section",
        "accordionSection",
    }
) | DROPPED_SECTIONS
