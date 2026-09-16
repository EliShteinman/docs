"""Mirroring redis.io's single-body document types.

Most of what redis.io publishes outside the documentation is not a
page-builder page: a glossary entry, a tutorial, a customer story and an
architecture diagram each carry their prose in one field. What differs between
them is which field, what the title is called, and whether the body arrives as
Portable Text or as markdown that was authored as markdown.

That is small enough to describe as data rather than as four readers, which is
what DocumentTree below is. Adding another type is an entry in TREES.

The tutorials are the reason this exists at all. There are 122 of them with a
median of 15,000 characters -- rate limiting, token storage, inventory
reservation -- and they are the densest technical writing Redis publishes
outside the docs.
"""

from __future__ import annotations

import json
import re
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from build.site_mirror.portable_text import ImageResolver, render

# Images inside a markdown body arrive as plain CDN URLs, not as references.
_MARKDOWN_IMAGE = re.compile(r"(!\[[^\]]*\]\()([^)\s]+)")


@dataclass(frozen=True)
class DocumentTree:
    """One body of content: where it lives, and how to read a document of it."""

    name: str
    doc_type: str
    prefix: str
    directory: Path
    # The section index to write. Every tree writes one, into a directory of
    # its own -- never into a section the documentation already owns. See the
    # glossary tree below for the one place that distinction had to be made.
    index: str
    title_field: str = "title"
    body_field: str = "body"
    body_is_markdown: bool = False
    # The document's own lead image, where the picture is the point: an
    # architecture diagram is a caption plus a diagram, and the caption alone
    # is not the content.
    lead_image_field: str = ""
    # A field to group the section index by, dereferenced from the source. An
    # index of 56 customer stories is a wall the same way the blog was; by
    # industry it is eight short lists.
    group_field: str = ""
    group_projection: str = ""
    # Hidden documents stay out of the sidebar and are reached from their
    # section index. Worth it past roughly a hundred entries.
    hidden: bool = False

    @property
    def projection(self) -> str:
        fields = {
            "_id",
            "_updatedAt",
            "pathname",
            self.title_field,
            self.body_field,
            "publishDate",
        }
        if self.lead_image_field:
            fields.add(self.lead_image_field)
        projected = sorted(fields)
        if self.group_projection:
            projected.append(self.group_projection)
        return "{" + ",".join(projected) + "}"


def localize_markdown_images(body: str, mirror_url: Callable[[str], str]) -> str:
    """Point the images embedded in a markdown body at the mirrored copies."""

    def replace(match: re.Match[str]) -> str:
        local = mirror_url(match.group(2))
        return match.group(1) + (local or match.group(2))

    return _MARKDOWN_IMAGE.sub(replace, body or "")


def render_document(
    tree: DocumentTree,
    document: dict,
    resolve_image: ImageResolver,
    mirror_url: Callable[[str], str],
) -> str:
    """Return the markdown body for one document."""
    body = document.get(tree.body_field)
    if tree.body_is_markdown:
        rendered = localize_markdown_images(body if isinstance(body, str) else "", mirror_url)
    else:
        rendered = render(body if isinstance(body, list) else [], resolve_image)
    lead = _lead_image(tree, document, resolve_image)
    return f"{lead}\n\n{rendered}".strip() if lead else rendered


def _lead_image(tree: DocumentTree, document: dict, resolve_image: ImageResolver) -> str:
    if not tree.lead_image_field:
        return ""
    field = document.get(tree.lead_image_field) or {}
    reference = ((field.get("asset") or {}).get("_ref")) or ""
    if not reference:
        return ""
    alt = field.get("altText") or document.get(tree.title_field) or ""
    path = resolve_image(reference, alt)
    return f"![{alt}]({path})" if path else ""


def title_of(tree: DocumentTree, document: dict) -> str:
    return (document.get(tree.title_field) or document.get("title") or "").strip()


def _index(title: str, blurb: str, url: str = "") -> str:
    """Return a section index page.

    `url` is set where the tree's documents do not live directly under the
    section's own path: the diagrams publish at /resources/architecture-diagrams/
    because that is where redis.io publishes them, so the index that lists them
    has to sit there too rather than at /architecture-diagrams/.
    """
    # Quoted, not bare: a blurb that mentions redis.io carries a colon, and an
    # unquoted colon makes the frontmatter invalid YAML and fails the build.
    return (
        "---\n"
        f"title: {json.dumps(title, ensure_ascii=False)}\n"
        f"linkTitle: {json.dumps(title, ensure_ascii=False)}\n"
        f"description: {json.dumps(blurb, ensure_ascii=False)}\n"
        + (f"url: {url}\n" if url else "")
        + "---\n\n"
        # The description is already rendered above the body by the layout;
        # repeating it here printed it twice on every index page.
        "<!-- Generated by build/site_mirror; edits here are overwritten "
        "by the next sync. -->\n"
    )


TREES: tuple[DocumentTree, ...] = (
    DocumentTree(
        name="tutorials",
        doc_type="tutorialItem",
        prefix="/tutorials/*",
        directory=Path("content/tutorials"),
        body_field="markdownBody",
        body_is_markdown=True,
        group_field="category",
        group_projection='"category":category->name',
        # 122 entries would crowd the sidebar the way the blog would; they are
        # reached from the index, from search, and from the docs links.
        hidden=True,
        index=_index(
            "Tutorials",
            "Step-by-step Redis tutorials: rate limiting, token storage, "
            "inventory reservation, caching and more.",
        ),
    ),
    DocumentTree(
        name="glossary",
        doc_type="glossaryItem",
        prefix="/glossary/*",
        # NOT content/glossary. That section is the documentation's own
        # glossary -- 188 hand-written definitions in the body of its
        # _index.md, rendered by an upstream layout -- and the mirror is an
        # addition to this site, never an edit to it. The terms still publish
        # at /glossary/<term>/, which is where redis.io publishes them and
        # which collides with nothing; only the listing page lives here,
        # because /glossary/ belongs to the documentation.
        directory=Path("content/redis-glossary"),
        title_field="term",
        index=_index(
            "Redis glossary",
            "Definitions of the terms Redis uses across its products.",
        ),
    ),
    DocumentTree(
        name="architecture-diagrams",
        doc_type="architectureDiagram",
        prefix="/resources/architecture-diagrams/*",
        directory=Path("content/architecture-diagrams"),
        body_field="content",
        lead_image_field="image",
        group_field="categories",
        group_projection='"categories":categories[]->title',
        index=_index(
            "Architecture diagrams",
            "Reference architectures for building on Redis.",
            url="/resources/architecture-diagrams/",
        ),
    ),
    DocumentTree(
        name="customers",
        doc_type="customerStory",
        prefix="/customers/*",
        directory=Path("content/customers"),
        hidden=True,
        group_field="industry",
        group_projection='"industry":industry->title',
        index=_index(
            "Customer stories",
            "How organisations run Redis in production.",
        ),
    ),
)
