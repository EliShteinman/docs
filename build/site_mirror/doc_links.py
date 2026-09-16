"""Resolving the links that point at redis.io for pages this image already has.

The mirrored posts and the documentation both link to redis.io by absolute URL,
and the build already rewrites the spellings it can rewrite by rule:
`/docs/latest/...`, `/commands/...`, and the sections the mirror publishes. What
is left over are the URLs no rule can straighten out:

  * **Legacy documentation paths.** `/docs/interact/search-and-query/...` and
    `/topics/pubsub` are where those pages lived before two restructurings.
    redis.io answers them with a redirect; this image answers them with a 404,
    so a reader inside the air gap loses a link to a page sitting on their own
    server. The target cannot be derived -- only redis.io knows where each one
    moved -- so it is *observed*: each URL is followed once, on a machine with
    the internet, and where it lands is written into doc_links.json and
    committed. A build then applies the map with no network at all.

  * **Everything else on redis.io**: /downloads, /try-free, /cloud, a booking
    form. Nothing mirrors those and nothing in the image serves them. Inside
    mirrored pages they are unlinked -- the words stay, the dead link goes --
    because a link that cannot resolve is worse than no link: it reads as
    something the reader is missing out on. The documentation's own pages are
    left alone; they are upstream's text, and rewriting their prose is not this
    fork's business.

Run in the build, after the rewrites that work by rule:

    python -m build.site_mirror.doc_links            # apply the map
    python -m build.site_mirror.doc_links --refresh  # re-observe; needs internet
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

from build.site_mirror.sanity import USER_AGENT

LOGGER = logging.getLogger("site_mirror.doc_links")

MAP_PATH = Path(__file__).with_name("doc_links.json")

# Every host the corpus spells redis.io with, including the two it used before.
_HOSTS = r"(?:www\.)?(?:redis\.io|redis\.com|redislabs\.com)"

# A legacy documentation URL: /docs/<anything but latest> or /topics/<page>.
LEGACY = re.compile(rf"https?://{_HOSTS}(?:/en)?(/(?:docs|topics)/(?!latest/)[A-Za-z0-9._/-]*)")

# Any remaining absolute link to redis.io, in a markdown link that is not an
# image. The `(?<!!)` keeps `![alt](...)` out of it: an image with no source is
# not an improvement on a broken one.
MARKETING_LINK = re.compile(rf"(?<!!)\[([^\]]+)\]\(\s*(https?://{_HOSTS}[^\s)]*)\s*\)")

# Paths another rewrite in the same build turns into local links: the current
# documentation, the command pages, and every section the mirror publishes.
# Never unlinked, whatever order the steps run in -- this step must not be the
# reason a link to a page in this very image stops being a link.
SERVED_BY_RULE = re.compile(
    r"^/(?:docs/latest|commands|blog|tutorials|glossary|compare|solutions"
    r"|customers|technology|resources/architecture-diagrams)(?:/|$)"
)

# What a mirrored file says about itself (build/site_mirror/hugo.py).
MIRROR_MARKER = "mirrored: true"

# Where the documentation lives in this image once the build's own rewrites have
# run: redis.io publishes it under /docs/latest/, this image at the root.
_DOCS_PREFIX = "https://redis.io/docs/latest/"


def is_mirrored(text: str) -> bool:
    """Whether this page was written by the mirror rather than by upstream."""
    if not text.startswith("---"):
        return False
    _, _, rest = text.partition("---")
    frontmatter, _, _ = rest.partition("\n---")
    return any(line.strip() == MIRROR_MARKER for line in frontmatter.splitlines())


def legacy_urls(content_root: Path) -> list[str]:
    """Return every distinct legacy documentation URL the content links to."""
    found: set[str] = set()
    for markdown in content_root.rglob("*.md"):
        text = markdown.read_text(encoding="utf-8", errors="replace")
        for match in LEGACY.finditer(text):
            found.add(match.group(0).split("#")[0].split("?")[0])
    return sorted(found)


def local_path(final_url: str) -> str:
    """Return the path this image serves `final_url` at, or "" if it serves none."""
    if not final_url.startswith(_DOCS_PREFIX):
        return ""
    path = "/" + final_url[len(_DOCS_PREFIX):]
    return path if path.endswith("/") else path + "/"


def observe(url: str, timeout: float) -> str:
    """Follow `url` on redis.io and return the local path it lands on."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return local_path(response.geturl())
    except (urllib.error.URLError, OSError) as error:
        LOGGER.warning("could not follow %s: %s", url, error)
        return ""


def published_paths(content_root: Path) -> set[str]:
    """Every path this site publishes: each page's own URL, and its aliases.

    Read from the content rather than from a build, so the map can be checked
    without one. A page's URL is its `url:` when it declares one and its path in
    the tree otherwise, which is what Hugo does with these sections.
    """
    # The home page has no content file of its own (config.toml builds it from
    # layouts), so it is named here rather than discovered.
    published: set[str] = {"/"}

    def add(path: str) -> None:
        cleaned = path.strip().strip('"').strip("'").split("#")[0].split("?")[0]
        if cleaned.startswith("/"):
            published.add(cleaned.rstrip("/") + "/")

    for markdown in content_root.rglob("*.md"):
        relative = markdown.relative_to(content_root)
        stem = relative.parent if relative.name == "_index.md" else relative.with_suffix("")
        add("/" + str(stem).strip(".").strip("/"))
        text = markdown.read_text(encoding="utf-8", errors="replace")
        if not text.startswith("---"):
            continue
        frontmatter = text.partition("---")[2].partition("\n---")[0]
        in_aliases = False
        for line in frontmatter.splitlines():
            if line.startswith("url:"):
                add(line.split(":", 1)[1])
            elif line.startswith("aliases:"):
                in_aliases = True
            elif in_aliases and line.lstrip().startswith("- "):
                add(line.lstrip()[2:])
            elif in_aliases and line and not line[0].isspace():
                in_aliases = False
    return published


def refresh(content_root: Path, timeout: float = 30.0) -> dict[str, str]:
    """Re-observe every legacy URL and return the map. Needs the internet.

    A URL is kept only when the page redis.io sends it to is one this site
    actually publishes. Replacing a link that fails outright with one that 404s
    inside the image would move the failure rather than fix it, and hide it
    behind a page that looks like it should have worked.
    """
    urls = legacy_urls(content_root)
    published = published_paths(content_root)
    LOGGER.info("%d distinct legacy URLs against %d published paths", len(urls), len(published))
    mapping: dict[str, str] = {}
    unserved = 0
    for url in urls:
        landed = observe(url, timeout)
        if not landed:
            continue
        if landed not in published:
            LOGGER.info("  %s lands on %s, which this site does not publish", url, landed)
            unserved += 1
            continue
        mapping[url] = landed
    LOGGER.info(
        "%d of %d resolved to a page this image serves (%d landed outside it)",
        len(mapping), len(urls), unserved,
    )
    return mapping


def load(path: Path = MAP_PATH) -> dict[str, str]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def save(mapping: dict[str, str], path: Path = MAP_PATH) -> None:
    path.write_text(json.dumps(mapping, indent=1, sort_keys=True) + "\n", encoding="utf-8")


def rewrite_legacy(text: str, mapping: dict[str, str]) -> tuple[str, int]:
    """Point every mapped legacy URL at the local page, keeping any fragment."""
    rewritten = 0

    def replace(match: re.Match) -> str:
        nonlocal rewritten
        whole = match.group(0)
        landed = mapping.get(whole)
        if not landed:
            return whole
        rewritten += 1
        return landed

    return LEGACY.sub(replace, text), rewritten


def unlink_unservable(text: str) -> tuple[str, int]:
    """Turn links this image cannot serve back into the words they were written as."""
    removed = 0

    def replace(match: re.Match) -> str:
        nonlocal removed
        url = match.group(2)
        path = re.sub(rf"^https?://{_HOSTS}(?:/en)?", "", url).split("#")[0].split("?")[0]
        if SERVED_BY_RULE.match(path or "/"):
            return match.group(0)
        removed += 1
        return match.group(1)

    return MARKETING_LINK.sub(replace, text), removed


def apply_to_tree(content_root: Path, mapping: dict[str, str]) -> tuple[int, int, int]:
    """Rewrite the content tree in place. Returns (files, legacy fixed, links removed)."""
    touched = legacy_total = removed_total = 0
    for markdown in content_root.rglob("*.md"):
        original = markdown.read_text(encoding="utf-8", errors="replace")
        text, legacy_count = rewrite_legacy(original, mapping)
        removed_count = 0
        # Only inside the mirror's own pages: the documentation's prose is
        # upstream's, and this fork rewrites its links, not its sentences.
        if is_mirrored(original):
            text, removed_count = unlink_unservable(text)
        if text != original:
            markdown.write_text(text, encoding="utf-8")
            touched += 1
        legacy_total += legacy_count
        removed_total += removed_count
    return touched, legacy_total, removed_total


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--content", type=Path, default=Path("content"))
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Follow every legacy URL on redis.io and rewrite the map. Needs the internet.",
    )
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--log-level", default="INFO")
    args = parser.parse_args(argv)
    logging.basicConfig(level=args.log_level.upper(), format="%(levelname)s %(name)s %(message)s")

    if args.refresh:
        save(refresh(args.content, args.timeout))
        LOGGER.info("wrote %s", MAP_PATH)
        return 0

    mapping = load()
    if not mapping:
        LOGGER.error("%s is empty or missing; run with --refresh on a connected machine", MAP_PATH)
        return 1
    touched, legacy, removed = apply_to_tree(args.content, mapping)
    LOGGER.info(
        "%d files rewritten: %d legacy links pointed inward, %d dead links unlinked",
        touched, legacy, removed,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
