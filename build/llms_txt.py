"""Writing the site's llms.txt from redis.io's, pointed at the pages this image has.

redis.io serves /llms.txt from its marketing site: an index for AI agents of the
documentation, the tutorials and redis.io's product pages. This image has the
documentation and, when the mirror is deployed, the mirrored sections -- not the
product pages. So the file is *observed*, like build/doc_links.json: fetched once
on a machine with the internet, every link this image can answer kept and the
rest dropped, and the result committed. The build serves it with no network.

Two files, because what the image answers depends on the mirror:

    static/llms.txt       with the mirror deployed
    static/llms-docs.txt  without it; nginx serves it as /llms.txt

A documentation link redis.io lists under a path the documentation has since
left is followed on redis.io to where it lands, the way doc_links does it. Links
are written with the __DOCS_BASE_URL__ placeholder nginx fills in per request,
like the Markdown feed's.

    python -m build.llms_txt   # needs the internet
"""

from __future__ import annotations

import argparse
import logging
import re
import sys
import urllib.error
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from build.doc_links import alias_targets, local_path, published_paths
from build.marketing_mirror import settings as mirror_settings

LOGGER = logging.getLogger("llms_txt")

SOURCE = "https://redis.io/llms.txt"
DOCS_PREFIX = "https://redis.io/docs/latest/"
PLACEHOLDER = "__DOCS_BASE_URL__"
USER_AGENT = "redis-docs-airgap-llms-txt/1.0"
STATIC_DIR = Path("static")
WITH_MIRROR = "llms.txt"
DOCS_ONLY = "llms-docs.txt"

MARKDOWN_SUFFIX = "index.html.md"
LINK = re.compile(r"\]\((https?://[^)\s]+)\)")
# Any link, rewritten or not: what a heading needs under it to stay.
LISTED = re.compile(r"\]\([^)\s]+\)")
HEADING = re.compile(r"^(#{2,6}) ")

FEEDS_HEADING = "## Full-text feeds"
DOCS_FEED = (
    f"- [Documentation feed]({PLACEHOLDER}/docs.ndjson): every documentation page as"
    " one JSON record per line, Markdown content included."
)
MIRROR_FEED = (
    f"- [Mirrored sections feed]({PLACEHOLDER}/mirror.ndjson): the blog, tutorials and"
    " the other mirrored redis.io sections, in the same shape."
)


@dataclass(frozen=True)
class Target:
    """Where a link points inside this image, and whether only the mirror answers it."""

    url: str
    mirrored: bool


class LinkResolver:
    """Decides, for each redis.io link, which page of this image answers it."""

    def __init__(
        self,
        published: set[str],
        aliases: dict[str, str],
        mirror_dir: Path,
        follow: Callable[[str], str],
    ) -> None:
        self._published = published
        self._aliases = aliases
        self._mirror_dir = mirror_dir
        self._follow = follow
        self._resolved: dict[str, Target | None] = {}

    def resolve(self, url: str) -> Target | None:
        # Both files are written from the same links: follow each one once.
        if url not in self._resolved:
            self._resolved[url] = (
                self._documentation(url)
                if url.startswith(DOCS_PREFIX)
                else self._mirrored(url)
            )
        return self._resolved[url]

    def _documentation(self, url: str) -> Target | None:
        path = url[len(DOCS_PREFIX) :]
        markdown = path.endswith(MARKDOWN_SUFFIX)
        page = "/" + path.removesuffix(MARKDOWN_SUFFIX)
        page = page if page.endswith("/") else page + "/"
        if not self._publishes(page):
            landed = local_path(self._follow(DOCS_PREFIX + page.lstrip("/")))
            if not landed or not self._publishes(landed):
                LOGGER.info("dropped, not a page of this site: %s", url)
                return None
            page = landed
        # An alias is only a redirect: link the page it redirects to.
        page = self._aliases.get(page, page)
        suffix = MARKDOWN_SUFFIX if markdown else ""
        return Target(f"{PLACEHOLDER}{page}{suffix}", mirrored=False)

    def _publishes(self, page: str) -> bool:
        """Whether Hugo publishes `page`.

        A top-level directory with no `_index.md` is not in published_paths, but
        Hugo still makes it a section (`/commands/`).
        """
        if page in self._published:
            return True
        top_level = page.count("/") == 2
        return top_level and any(path.startswith(page) for path in self._published)

    def _mirrored(self, url: str) -> Target | None:
        path = "/" + url.split("://", 1)[1].partition("/")[2]
        if not url.startswith(mirror_settings.ORIGIN + "/") or not any(
            path.startswith(section) for section in mirror_settings.SECTIONS
        ):
            LOGGER.info("dropped, not mirrored: %s", url)
            return None
        relative = path.strip("/")
        if not (
            (self._mirror_dir / relative).is_file()
            or (self._mirror_dir / relative / "index.html").is_file()
        ):
            LOGGER.warning("dropped, in a mirrored section but not on disk: %s", url)
            return None
        return Target(f"{PLACEHOLDER}{path}", mirrored=True)


def rewrite(source: str, resolver: LinkResolver, with_mirror: bool) -> str:
    """Return redis.io's llms.txt with every link this image answers, and only those."""
    kept: list[str] = []
    for line in source.splitlines():
        match = LINK.search(line)
        if match is None:
            kept.append(line)
            continue
        target = resolver.resolve(match.group(1))
        if target is None or (target.mirrored and not with_mirror):
            continue
        kept.append(line[: match.start(1)] + target.url + line[match.end(1) :])
    lines = _drop_empty_sections(kept)
    lines += ["", FEEDS_HEADING, "", DOCS_FEED]
    if with_mirror:
        lines.append(MIRROR_FEED)
    return "\n".join(lines) + "\n"


def _drop_empty_sections(lines: list[str]) -> list[str]:
    """Remove each heading no link survived under, down to its next sibling or parent."""
    result: list[str] = []
    for index, line in enumerate(lines):
        heading = HEADING.match(line)
        if heading and not _has_links_under(lines, index, len(heading.group(1))):
            continue
        result.append(line)
    return _collapse_blank_lines(result)


def _has_links_under(lines: list[str], index: int, level: int) -> bool:
    for line in lines[index + 1 :]:
        heading = HEADING.match(line)
        if heading and len(heading.group(1)) <= level:
            return False
        if LISTED.search(line):
            return True
    return False


def _collapse_blank_lines(lines: list[str]) -> list[str]:
    collapsed: list[str] = []
    for line in lines:
        if not line.strip() and collapsed and not collapsed[-1].strip():
            continue
        collapsed.append(line)
    while collapsed and not collapsed[-1].strip():
        collapsed.pop()
    return collapsed


def fetch(url: str, timeout: float) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8")


def follow(url: str, timeout: float) -> str:
    """Return where redis.io sends `url`, or "" if it cannot be followed."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.geturl()
    except (urllib.error.URLError, OSError) as error:
        LOGGER.warning("could not follow %s: %s", url, error)
        return ""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--content", type=Path, default=Path("content"))
    parser.add_argument("--mirror", type=Path, default=mirror_settings.SITE_DIR)
    parser.add_argument("--output", type=Path, default=STATIC_DIR)
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--log-level", default="INFO")
    args = parser.parse_args(argv)
    logging.basicConfig(
        level=args.log_level.upper(), format="%(levelname)s %(name)s %(message)s"
    )

    try:
        source = fetch(SOURCE, args.timeout)
    except (urllib.error.URLError, OSError) as error:
        LOGGER.error("could not fetch %s: %s", SOURCE, error)
        return 1
    resolver = LinkResolver(
        published_paths(args.content),
        alias_targets(args.content),
        args.mirror,
        lambda url: follow(url, args.timeout),
    )
    for name, with_mirror in ((WITH_MIRROR, True), (DOCS_ONLY, False)):
        text = rewrite(source, resolver, with_mirror)
        (args.output / name).write_text(text, encoding="utf-8")
        LOGGER.info("wrote %s: %d links", args.output / name, len(LISTED.findall(text)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
