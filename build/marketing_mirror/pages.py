"""One page: its HTML as redis.io renders it, and its Markdown twin.

redis.io publishes every page as Markdown at the same path plus `.md`; the
page's own "View as Markdown" link points there, and the search feed is built
from it (feed.py). A page without one (a listing, an author page) is mirrored
anyway -- it is the Markdown that is optional, not the page.
"""

from __future__ import annotations

import logging
from pathlib import Path

from build.marketing_mirror import rewrite, settings
from build.marketing_mirror.assets import AssetStore
from build.marketing_mirror.fetcher import FetchError, Fetcher

LOGGER = logging.getLogger("marketing_mirror")


def html_file(site_dir: Path, path: str) -> Path:
    return site_dir / path.strip("/") / "index.html"


def markdown_file(site_dir: Path, path: str) -> Path:
    return site_dir / (path.strip("/") + ".md")


class PageMirror:
    def __init__(self, fetcher: Fetcher, assets: AssetStore, site_dir: Path) -> None:
        self._fetcher = fetcher
        self._assets = assets
        self._site_dir = site_dir

    def capture(self, path: str) -> None:
        """Mirror one page. Raises FetchError when the page itself cannot be read."""
        html = self._fetcher.get(settings.ORIGIN + path).decode("utf-8")
        self._assets.add_next(rewrite.next_assets(html))
        self._assets.add_sanity(rewrite.sanity_assets(html))
        self._write(
            html_file(self._site_dir, path), rewrite.rewrite_page(html).encode("utf-8")
        )
        self._capture_markdown(path)

    def _capture_markdown(self, path: str) -> None:
        url = settings.ORIGIN + path.rstrip("/") + ".md"
        try:
            markdown = self._fetcher.get(url)
        except FetchError as error:
            LOGGER.debug("no markdown for %s: %s", path, error)
            return
        local = markdown.replace(
            (settings.SANITY_CDN + "/").encode(),
            (settings.LOCAL_SANITY_PREFIX + "/").encode(),
        )
        self._write(markdown_file(self._site_dir, path), local)

    @staticmethod
    def _write(target: Path, data: bytes) -> None:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
