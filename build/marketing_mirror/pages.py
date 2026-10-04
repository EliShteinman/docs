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
from build.marketing_mirror.assets import AssetStore, place
from build.marketing_mirror.embeds import EmbedMirror
from build.marketing_mirror.fetcher import FetchError, Fetcher
from build.marketing_mirror.manifest import Manifest

LOGGER = logging.getLogger("marketing_mirror")


def html_file(site_dir: Path, path: str) -> Path:
    return site_dir / path.strip("/") / "index.html"


def markdown_file(site_dir: Path, path: str) -> Path:
    return site_dir / (path.strip("/") + ".md")


class PageMirror:
    def __init__(
        self,
        fetcher: Fetcher,
        assets: AssetStore,
        embeds: EmbedMirror,
        site_dir: Path,
        previous_dir: Path | None = None,
        previous: Manifest | None = None,
    ) -> None:
        self._fetcher = fetcher
        self._assets = assets
        self._embeds = embeds
        self._site_dir = site_dir
        self._previous_dir = previous_dir
        self._previous = previous or Manifest()

    def capture(self, path: str, lastmod: str = "") -> bool:
        """Mirror one page; True when it was fetched, False when taken from disk.

        Raises FetchError when a page that has to be fetched cannot be read.
        """
        if self._reuse(path, lastmod):
            return False
        html = self._fetcher.get(settings.ORIGIN + path).decode("utf-8")
        self._assets.add_next(rewrite.next_assets(html))
        self._assets.add_sanity(rewrite.sanity_assets(html))
        local = rewrite.rewrite_page(html)
        self._embeds.add(rewrite.local_embed_pages(local))
        self._write(html_file(self._site_dir, path), local.encode("utf-8"))
        self._capture_markdown(path)
        return True

    def _reuse(self, path: str, lastmod: str) -> bool:
        if self._previous_dir is None or not self._previous.is_current(path, lastmod):
            return False
        previous_html = html_file(self._previous_dir, path)
        if not previous_html.is_file():
            return False
        html = previous_html.read_text(encoding="utf-8")
        self._assets.add_next(rewrite.next_assets(html))
        self._assets.add_sanity(rewrite.sanity_assets(html))
        local = rewrite.rewrite_again(html)
        self._embeds.add(rewrite.local_embed_pages(local))
        if local == html:
            place(previous_html, html_file(self._site_dir, path))
        else:
            self._write(html_file(self._site_dir, path), local.encode("utf-8"))
        previous_markdown = markdown_file(self._previous_dir, path)
        if previous_markdown.is_file():
            place(previous_markdown, markdown_file(self._site_dir, path))
        return True

    def _capture_markdown(self, path: str) -> None:
        url = settings.ORIGIN + path.rstrip("/") + ".md"
        try:
            markdown = self._fetcher.get(url)
        except FetchError as error:
            LOGGER.debug("no markdown for %s: %s", path, error)
            return
        if markdown.lstrip()[:15].lower().startswith((b"<!doctype", b"<html")):
            # redis.io answers a moved page's .md with a redirect to some other
            # page's HTML; that is not this page's Markdown.
            LOGGER.debug("no markdown for %s: got an HTML page instead", path)
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
