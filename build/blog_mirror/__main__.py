"""Run the blog mirror: fetch, convert, and write into the content tree.

    python -m build.blog_mirror [--content DIR] [--images DIR] [--limit N]

Run from the repository root before Hugo builds. It is idempotent: posts are
rewritten from the source every time, and an image already on disk is not
fetched again, so a re-run after an interrupted one only does what is left.
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from build.blog_mirror import hugo, portable_text
from build.blog_mirror.images import ImageMirror
from build.blog_mirror.sanity import SanityError, count_posts, fetch_posts

LOGGER = logging.getLogger("blog_mirror")


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
    parser.add_argument("--timeout", type=float, default=60.0)
    parser.add_argument("--log-level", default="INFO")
    return parser.parse_args(argv)


def mirror(content_dir: Path, image_dir: Path, limit: int, timeout: float) -> int:
    """Mirror every post. Returns the number written."""
    expected = count_posts(timeout)
    LOGGER.info("source holds %d posts", expected)
    images = ImageMirror(image_dir, timeout)
    written: set[str] = set()

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
        hugo.write_post(content_dir, name, hugo.render_post(post, body))
        written.add(name)
        if index % 100 == 0:
            LOGGER.info("%d/%d posts written, %d images fetched", index, expected, images.fetched)

    hugo.write_section_index(content_dir)
    if not limit:
        hugo.prune_removed(content_dir, written)
    LOGGER.info(
        "done: %d posts, %d images fetched, %d already present, %d failed",
        len(written), images.fetched, images.skipped, len(images.failed),
    )
    if images.failed:
        LOGGER.warning("images that could not be fetched: %s", ", ".join(images.failed[:10]))
    return len(written)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    logging.basicConfig(
        level=args.log_level.upper(),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    try:
        written = mirror(args.content, args.images, args.limit, args.timeout)
    except SanityError as error:
        LOGGER.critical("blog mirror failed: %s", error)
        return 1
    return 0 if written else 1


if __name__ == "__main__":
    sys.exit(main())
