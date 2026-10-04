"""Framed pages redis.io serves from elsewhere, served from this site instead.

A page under settings.LOCAL_EMBEDS is plain static files: the page, the files
next to it, and a library from a CDN. All of it is captured, and the page is
rewritten to load each from here. Stylesheet imports are dropped: redis.io's
own copies of these answer them with 403, and the rest are web fonts.
"""

from __future__ import annotations

import logging
import re
import threading
from pathlib import Path
from urllib.parse import urljoin, urlsplit

from build.marketing_mirror import settings
from build.marketing_mirror.fetcher import FetchError, Fetcher

LOGGER = logging.getLogger("marketing_mirror")

_REFERENCE = re.compile(r'\b(?:src|href)="([^"]+)"')
# A file an inline script loads by a path next to the page: the charts fetch
# their data as './pure-vectors.json'.
_SCRIPT_REFERENCE = re.compile(r"""['"](\.{1,2}/[^'"\s]+\.\w+)['"]""")
_CSS_IMPORT = re.compile(r"@import\s*(?:url\()?\s*[\"'][^\"']*[\"']\s*\)?[^;]*;?")
_NOT_A_FILE = ("#", "data:", "mailto:", "javascript:")


def origin_url(local_path: str) -> str:
    """The URL redis.io frames for a path under a settings.LOCAL_EMBEDS prefix."""
    for origin, prefix in settings.LOCAL_EMBEDS.items():
        if local_path.startswith(prefix + "/"):
            return origin + local_path.removeprefix(prefix)
    raise ValueError(f"not a local embed: {local_path}")


def vendor_path(url: str) -> str:
    """Where a file a framed page loads from another host is kept."""
    parts = urlsplit(url if not url.startswith("//") else "https:" + url)
    return f"{settings.EMBED_VENDOR_PREFIX}/{parts.netloc}{parts.path}"


def strip_imports(stylesheet: str) -> str:
    return _CSS_IMPORT.sub("", stylesheet)


class EmbedMirror:
    def __init__(self, fetcher: Fetcher, site_dir: Path) -> None:
        self._fetcher = fetcher
        self._site_dir = site_dir
        self._lock = threading.Lock()
        self._claimed: set[str] = set()
        self.failed: set[str] = set()

    @property
    def count(self) -> int:
        return len(self._claimed) - len(self.failed)

    def add(self, local_pages: set[str]) -> None:
        for local_page in sorted(local_pages):
            if self._claim(local_page):
                self._capture_page(local_page)

    def write_unavailable_page(self) -> None:
        self._write(
            settings.EMBED_UNAVAILABLE,
            settings.EMBED_UNAVAILABLE_SOURCE.read_bytes(),
        )

    def _claim(self, path: str) -> bool:
        with self._lock:
            if path in self._claimed:
                return False
            self._claimed.add(path)
            return True

    def _capture_page(self, local_page: str) -> None:
        page_url = origin_url(local_page)
        data = self._fetch(page_url, local_page)
        if data is None:
            return
        page = data.decode("utf-8", "replace")
        references = set(_REFERENCE.findall(page)) | set(
            _SCRIPT_REFERENCE.findall(page)
        )
        for reference in sorted(references):
            page = self._capture_reference(page, page_url, local_page, reference)
        self._write(local_page, page.encode("utf-8"))

    def _capture_reference(
        self, page: str, page_url: str, local_page: str, reference: str
    ) -> str:
        if reference.startswith(_NOT_A_FILE):
            return page
        if reference.startswith(("http://", "https://", "//")):
            local = vendor_path(reference)
            self._capture_file(reference, local)
            return page.replace(f'"{reference}"', f'"{local}"')
        url = urljoin(page_url, reference)
        local = urljoin(local_page, reference)
        self._capture_file(url, local)
        return page

    def _capture_file(self, url: str, local: str) -> None:
        if not self._claim(local):
            return
        data = self._fetch(url if not url.startswith("//") else "https:" + url, local)
        if data is None:
            return
        if local.endswith(".css"):
            data = strip_imports(data.decode("utf-8", "replace")).encode("utf-8")
        self._write(local, data)

    def _fetch(self, url: str, local: str) -> bytes | None:
        try:
            return self._fetcher.get(url)
        except FetchError as error:
            LOGGER.warning("embedded file not mirrored: %s", error)
            with self._lock:
                self.failed.add(local)
            return None

    def _write(self, local: str, data: bytes) -> None:
        target = self._site_dir / local.lstrip("/")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
