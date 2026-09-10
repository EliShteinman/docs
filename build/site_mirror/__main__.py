"""Run the site mirror: fetch, convert, and write into the content tree.

    python -m build.site_mirror [--only blog|technology] [--limit N]

Two bodies of content, one pipeline. The blog is 1,109 posts of Portable Text;
/technology/ is eleven page-builder pages whose prose is spread across layout
sections (see pages.py). Both end up as Hugo pages under the paths redis.io
publishes them at.

Run from the repository root before Hugo builds. It is idempotent: documents
are rewritten from the source every time, and an image already on disk is not
fetched again, so a re-run after an interrupted one only does what is left.
"""

from __future__ import annotations

import argparse
import logging
import re
import sys
from pathlib import Path

from build.site_mirror import categories, documents, hugo, pages, portable_text, redirects
from build.site_mirror.images import ImageMirror
from build.site_mirror.sanity import (
    SanityError,
    count_documents,
    count_pages,
    count_posts,
    fetch_documents,
    fetch_pages,
    fetch_posts,
)

# The page tree mirrored alongside the blog. Kept as a list so adding another
# tree is a line here rather than a new code path.
PAGE_TREES = (
    ("technology", "/technology/*", hugo.TECHNOLOGY_DIR, hugo.TECHNOLOGY_INDEX),
    ("compare", "/compare/*", hugo.COMPARE_DIR, hugo.COMPARE_INDEX),
    ("solutions", "/solutions/*", hugo.SOLUTIONS_DIR, hugo.SOLUTIONS_INDEX),
)

LOGGER = logging.getLogger("site_mirror")


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--content", type=Path, default=hugo.SECTION_DIR)
    parser.add_argument("--images", type=Path, default=hugo.IMAGE_DIR)
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Stop after N posts. For trying the pipeline without fetching 2,900 images.",
    )
    parser.add_argument(
        "--only",
        choices=("blog", "technology", "compare", "solutions",
                 "tutorials", "glossary", "architecture-diagrams", "customers"),
        help="Mirror one body of content instead of all of them.",
    )
    parser.add_argument(
        "--refresh-redirects",
        action="store_true",
        help="Follow the stale links on redis.io and record where they land. "
             "Needs the public internet; run it deliberately, then commit the map.",
    )
    parser.add_argument("--timeout", type=float, default=60.0)
    parser.add_argument("--log-level", default="INFO")
    return parser.parse_args(argv)


def mirror_blog(
    content_dir: Path, images: ImageMirror, limit: int, timeout: float,
    redirect_map: dict[str, list[str]],
) -> int:
    """Mirror every blog post. Returns the number written."""
    expected = count_posts(timeout)
    LOGGER.info("source holds %d posts", expected)
    written: set[str] = set()
    category_counts: dict[str, int] = {}

    for index, post in enumerate(fetch_posts(timeout), start=1):
        if limit and index > limit:
            break
        name = hugo.file_name(post.get("slug") or "", post.get("_id") or f"post-{index}")
        body = portable_text.render(
            post.get("content") or [],
            lambda reference, _alt: images.ensure(reference),
        )
        # A post's own tile image is the one picture the page leads with; the
        # rest come from the body via the resolver above.
        lead = ((post.get("image") or {}).get("asset") or {}).get("_ref")
        if lead:
            path = images.ensure(lead)
            if path:
                alt = (post.get("image") or {}).get("altText") or post.get("title") or ""
                body = f"![{alt}]({path})\n\n{body}"
        hugo.write_post(
            content_dir,
            name,
            hugo.render_post(
                post, body, aliases=_aliases(hugo.permalink(post.get("slug") or ""), "", redirect_map)
            ),
        )
        written.add(name)
        for category in post.get("categories") or []:
            if category:
                category_counts[category] = category_counts.get(category, 0) + 1
        if index % 100 == 0:
            LOGGER.info("%d/%d posts written, %d images fetched", index, expected, images.fetched)

    hugo.write_section_index(content_dir)
    if not limit:
        hugo.prune_removed(content_dir, written)
        mirror_categories(
            categories.BLOG, "/blog/category/*", categories.INDEX,
            "posts from the Redis blog", category_counts, timeout,
        )
    return len(written)


# Sections whose links are worth resolving: the ones this mirror publishes.
MIRRORED_SECTIONS = (
    "blog", "tutorials", "glossary", "compare", "solutions",
    "customers", "technology", "resources/architecture-diagrams",
)

_LINK = re.compile(
    r"\]\((?:https?://(?:www\.)?redis\.io)?(/(?:"
    + "|".join(MIRRORED_SECTIONS)
    + r")/[A-Za-z0-9._/-]*)"
)


def _known_urls(content_root: Path) -> set[str]:
    """Return every path this mirror publishes, read back from what it wrote.

    Only the frontmatter is scanned, and only until it closes: a `url:` further
    down is body text, not a declaration.
    """
    known = set()
    for markdown in content_root.rglob("*.md"):
        lines = markdown.read_text(encoding="utf-8", errors="replace").split("\n")
        if not lines or lines[0].strip() != "---":
            continue
        for line in lines[1:]:
            if line.strip() == "---":
                break
            if line.startswith("url:"):
                known.add(line.split(":", 1)[1].strip().strip('"').rstrip("/") + "/")
                break
    return known


def _stale_targets(content_root: Path, known: set[str]) -> list[str]:
    """Return the internal links that point at a mirrored section but nothing in it."""
    seen = set()
    for markdown in content_root.rglob("*.md"):
        text = markdown.read_text(encoding="utf-8", errors="replace")
        for match in _LINK.finditer(text):
            target = match.group(1).split("#")[0].rstrip("/") + "/"
            if target not in known:
                seen.add(target)
    return sorted(seen)


def _aliases(pathname: str, flattened: str, redirect_map: dict[str, list[str]]) -> tuple[str, ...]:
    """Every stale URL that should land on this document."""
    found = list(redirects.aliases_for(pathname, redirect_map))
    if flattened and flattened not in found:
        found.append(flattened)
    return tuple(found)


def _under(prefix: str, pathname: str) -> str:
    """Return the sub-path of `pathname` under `prefix`, or "" if it is not under it.

    GROQ's `match` is token-based rather than a prefix test, so a query for
    "/solutions/*" also returns /tutorials/howtos/solutions/... . This is what
    keeps those out of the wrong tree.
    """
    root = "/" + prefix.strip("/*").strip("/") + "/"
    if not pathname.startswith(root):
        return ""
    return pathname[len(root):].strip("/")


def mirror_pages(
    name: str,
    prefix: str,
    content_dir: Path,
    index_text: str,
    images: ImageMirror,
    limit: int,
    timeout: float,
    redirect_map: dict[str, list[str]],
) -> int:
    """Mirror one page tree. Returns the number written."""
    expected = count_pages(prefix, timeout)
    LOGGER.info("source holds %d %s pages", expected, name)
    written: set[str] = set()
    unknown: set[str] = set()

    for index, page in enumerate(fetch_pages(prefix, timeout), start=1):
        if limit and index > limit:
            break
        pathname = (page.get("pathname") or "").strip()
        under = _under(prefix, pathname)
        # The tree's own root page becomes the section index, not a child of it,
        # and anything the token match dragged in is not ours.
        if not under:
            continue
        unknown |= pages.section_types(page) - pages.KNOWN_SECTIONS
        body = pages.render_page(page, lambda reference, _alt: images.ensure(reference))
        if not body.strip():
            LOGGER.warning("%s rendered empty; skipping", pathname)
            continue
        file = hugo.file_name(under, page.get("_id") or f"page-{index}")
        # Pages stay visible in the sidebar: eleven entries is a section a
        # reader can use, unlike 1,100 posts.
        alias = hugo.flattened_alias(name, under)
        hugo.write_post(
            content_dir,
            file,
            hugo.render_post(
                page, body, url=pathname, hidden=False,
                aliases=_aliases(pathname, alias, redirect_map),
            ),
        )
        written.add(file)

    hugo.write_section_index(content_dir, index_text)
    if not limit:
        hugo.prune_removed(content_dir, written)
    if unknown:
        # Not fatal: an unrecognised section contributes nothing, so the page
        # loses a block rather than gaining a broken one. Worth saying out loud
        # because it means the source grew a layout this reader does not know.
        LOGGER.warning("unrendered section types in %s: %s", name, ", ".join(sorted(unknown)))
    return len(written)


def mirror_categories(
    catalog: categories.CategorySet,
    prefix: str,
    index_text: str,
    noun: str,
    counts: dict[str, int],
    timeout: float,
) -> int:
    """Mirror a tree's category pages, at the URLs the source publishes them at."""
    written: set[str] = set()
    for document in fetch_documents(catalog.doc_type, prefix, catalog.projection, timeout):
        category = categories.to_category(document, catalog.title_field)
        if not category:
            continue
        hugo.write_post(
            catalog.directory,
            category.file_name,
            categories.render(category, counts.get(category.title, 0), noun),
        )
        written.add(category.file_name)
    hugo.write_section_index(catalog.directory, index_text)
    hugo.prune_removed(catalog.directory, written)
    LOGGER.info("%d %s categories", len(written), catalog.doc_type)
    return len(written)


def mirror_documents(
    tree: documents.DocumentTree, images: ImageMirror, limit: int, timeout: float,
    redirect_map: dict[str, list[str]],
) -> int:
    """Mirror one single-body document tree. Returns the number written."""
    expected = count_documents(tree.doc_type, tree.prefix, timeout)
    LOGGER.info("source holds %d %s documents", expected, tree.name)
    written: set[str] = set()
    group_counts: dict[str, int] = {}

    for index, document in enumerate(
        fetch_documents(tree.doc_type, tree.prefix, tree.projection, timeout), start=1
    ):
        if limit and index > limit:
            break
        pathname = (document.get("pathname") or "").strip()
        under = _under(tree.prefix, pathname)
        if not under:
            continue
        title = documents.title_of(tree, document)
        if not title:
            LOGGER.warning("%s has no title; skipping", pathname)
            continue
        body = documents.render_document(
            tree,
            document,
            lambda reference, _alt: images.ensure(reference),
            images.ensure_url,
        )
        if not body.strip():
            LOGGER.warning("%s rendered empty; skipping", pathname)
            continue
        # The tree may name its title something else (`term`), and the rest of
        # the writer reads `title`; the group value is normalised the same way.
        group = (document.get(tree.group_field) or "") if tree.group_field else ""
        # A tree may file a document under several categories (the diagrams do);
        # the index groups by one, so the first is the one that counts.
        if isinstance(group, list):
            group = next((g for g in group if g), "")
        if group:
            group_counts[group] = group_counts.get(group, 0) + 1
        document = {**document, "title": title, "group": group}
        file = hugo.file_name(under, document.get("_id") or f"doc-{index}")
        alias = hugo.flattened_alias(tree.directory.name, under)
        hugo.write_post(
            tree.directory,
            file,
            hugo.render_post(
                document, body, url=pathname, hidden=tree.hidden,
                aliases=_aliases(pathname, alias, redirect_map),
            ),
        )
        written.add(file)

    if tree.name == "tutorials" and not limit:
        mirror_categories(
            categories.TUTORIALS, "/tutorials/category/*", categories.TUTORIAL_INDEX,
            "tutorials", group_counts, timeout,
        )
    if tree.index is not None:
        hugo.write_section_index(tree.directory, tree.index)
    if not limit:
        hugo.prune_removed(tree.directory, written)
    return len(written)


def mirror(content_dir: Path, image_dir: Path, limit: int, timeout: float, only: str | None) -> int:
    """Mirror every configured body of content. Returns the number written."""
    images = ImageMirror(image_dir, timeout)
    redirect_map = redirects.load()
    if redirect_map:
        LOGGER.info("applying %d recorded redirects", sum(len(v) for v in redirect_map.values()))
    written = 0
    if only in (None, "blog"):
        written += mirror_blog(content_dir, images, limit, timeout, redirect_map)
    for name, prefix, directory, index_text in PAGE_TREES:
        if only in (None, name):
            written += mirror_pages(
                name, prefix, directory, index_text, images, limit, timeout, redirect_map
            )
    for tree in documents.TREES:
        if only in (None, tree.name):
            written += mirror_documents(tree, images, limit, timeout, redirect_map)
    LOGGER.info(
        "done: %d documents, %d images fetched (%d shrunk), %d already present, %d failed",
        written, images.fetched, images.converted, images.skipped, len(images.failed),
    )
    if images.failed:
        LOGGER.warning("images that could not be fetched: %s", ", ".join(images.failed[:10]))
    return written


def refresh_redirects(content_root: Path, timeout: float) -> int:
    """Follow every stale internal link on redis.io and record where it lands."""
    known = _known_urls(content_root)
    stale = _stale_targets(content_root, known)
    LOGGER.info("%d published paths, %d links pointing at none of them", len(known), len(stale))
    mapping, unrecovered = redirects.build_map(stale, known, timeout)
    redirects.save(mapping)
    recovered = sum(len(v) for v in mapping.values())
    LOGGER.info("recovered %d of %d; %d still lead nowhere", recovered, len(stale), len(unrecovered))
    for path_ in unrecovered[:10]:
        LOGGER.info("  unrecovered: %s", path_)
    return recovered


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    logging.basicConfig(
        level=args.log_level.upper(),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    if args.refresh_redirects:
        refresh_redirects(Path("content"), args.timeout)
        return 0
    try:
        written = mirror(args.content, args.images, args.limit, args.timeout, args.only)
    except SanityError as error:
        LOGGER.critical("site mirror failed: %s", error)
        return 1
    return 0 if written else 1


if __name__ == "__main__":
    sys.exit(main())
