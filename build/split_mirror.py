"""Splitting the mirrored sections out of the built site, into a tree of their own.

The mirror is 1,400 pages and 238 MB of pictures that a deployment may not want
at all, and until now the only way to have the documentation was to have them
too: one Hugo run, one output tree, one image. Hugo still runs once -- the pages
cross-reference each other and the layouts are shared, so building them apart
would mean building twice -- and what changes is what happens afterwards. The
finished tree is divided in two, and each half is wrapped in an image of its
own.

The glossary stays with the documentation. Its terms publish inside
/glossary/, the documentation's own section, so there is no path that separates
them; 57 short pages are not worth a split that would have to carve up a
section by which file wrote it.

Two things travel with the pages:

  * `/images/site-mirror/`, the pictures, which is nearly all of the weight.
  * The pages' records in the RAG feed, moved into a feed of the mirror's own.
    Left in place, the search service would index and return a blog post the
    site is no longer serving.

The sitemap is filtered the same way, so the documentation does not advertise
addresses it cannot answer.

    python3 build/split_mirror.py [--site public] [--mirror public-mirror]
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import shutil
import sys
from pathlib import Path

LOGGER = logging.getLogger("split_mirror")

# The sections build/site_mirror publishes, spelled as they are *published*
# rather than as their content directories are named. The two differ, and the
# difference is the whole correctness of this file:
#
#   content/architecture-diagrams  ->  /resources/architecture-diagrams/
#   content/blog-categories        ->  /blog/category/       (inside /blog/)
#   content/tutorial-categories    ->  /tutorials/category/  (inside /tutorials/)
#   content/redis-glossary         ->  /glossary/            (the docs' section)
#
# So the category trees need no entry of their own, and the glossary is
# deliberately absent -- see the module docstring.
MIRRORED_SECTIONS = (
    "blog",
    "tutorials",
    "compare",
    "solutions",
    "customers",
    "technology",
    "resources/architecture-diagrams",
)

# Where build/site_mirror/images.py puts the pictures it fetches.
IMAGE_DIR = "images/site-mirror"

MOVED = MIRRORED_SECTIONS + (IMAGE_DIR,)

FEED_NAME = "docs.ndjson"
# The mirror's own feed. Never served -- nginx routes only the section paths to
# the mirror pod -- but read out of the image by the search pod's init
# container, the same way the documentation's feed is.
MIRROR_FEED_NAME = "mirror.ndjson"

SITEMAP_NAME = "sitemap.xml"

_URL_PATH = re.compile(r"https?://[^/]+(/.*)$")


def path_of(url: str) -> str:
    """Return the site-relative path of a feed or sitemap URL."""
    match = _URL_PATH.match(url.strip())
    path = match.group(1) if match else url.strip()
    return path.split("#")[0].split("?")[0]


def belongs_to_mirror(url: str) -> bool:
    """Whether this URL is one of the pages moving out of the site tree."""
    path = path_of(url).lstrip("/")
    return any(path == section or path.startswith(section + "/") for section in MOVED)


def move_sections(site: Path, mirror: Path) -> list[str]:
    """Move each mirrored section out of `site` and into `mirror`."""
    moved = []
    for section in MOVED:
        source = site / section
        if not source.is_dir():
            continue
        destination = mirror / section
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists():
            shutil.rmtree(destination)
        shutil.move(str(source), str(destination))
        moved.append(section)
    return moved


def split_feed(site: Path, mirror: Path) -> tuple[int, int]:
    """Divide the RAG feed. Returns (records kept, records moved)."""
    feed = site / FEED_NAME
    if not feed.is_file():
        LOGGER.warning("%s is not there; nothing to divide", feed)
        return 0, 0
    kept: list[str] = []
    moved: list[str] = []
    for line in feed.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            url = json.loads(line).get("url") or ""
        except json.JSONDecodeError:
            # A line that cannot be read stays with the documentation rather
            # than being dropped: this step divides a feed, it does not filter
            # one.
            kept.append(line)
            continue
        (moved if belongs_to_mirror(url) else kept).append(line)
    feed.write_text("\n".join(kept) + "\n", encoding="utf-8")
    mirror.mkdir(parents=True, exist_ok=True)
    (mirror / MIRROR_FEED_NAME).write_text("\n".join(moved) + "\n", encoding="utf-8")
    return len(kept), len(moved)


def split_sitemap(site: Path, mirror: Path) -> int:
    """Drop the moved pages from the site's sitemap. Returns how many went."""
    sitemap = site / SITEMAP_NAME
    if not sitemap.is_file():
        return 0
    text = sitemap.read_text(encoding="utf-8")
    dropped = 0

    def keep(match: re.Match) -> str:
        nonlocal dropped
        location = re.search(r"<loc>(.*?)</loc>", match.group(0), re.S)
        if location and belongs_to_mirror(location.group(1)):
            dropped += 1
            return ""
        return match.group(0)

    text = re.sub(r"<url>.*?</url>", keep, text, flags=re.S)
    sitemap.write_text(text, encoding="utf-8")
    return dropped


def split(site: Path, mirror: Path) -> dict[str, int]:
    """Divide a built site tree in two. Returns what was done, for the log."""
    moved = move_sections(site, mirror)
    kept_records, moved_records = split_feed(site, mirror)
    dropped = split_sitemap(site, mirror)
    return {
        "sections": len(moved),
        "feed_kept": kept_records,
        "feed_moved": moved_records,
        "sitemap_dropped": dropped,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", type=Path, default=Path("public"))
    parser.add_argument("--mirror", type=Path, default=Path("public-mirror"))
    parser.add_argument("--log-level", default="INFO")
    args = parser.parse_args(argv)
    logging.basicConfig(level=args.log_level.upper(), format="%(levelname)s %(name)s %(message)s")

    if not args.site.is_dir():
        LOGGER.error("%s is not a built site tree", args.site)
        return 1
    result = split(args.site, args.mirror)
    LOGGER.info(
        "moved %d sections and %d feed records into %s; %d records and the rest of the "
        "sitemap stay with the documentation (%d addresses dropped from it)",
        result["sections"], result["feed_moved"], args.mirror,
        result["feed_kept"], result["sitemap_dropped"],
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
