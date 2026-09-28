"""The files the pages load: Next.js chunks, stylesheets, fonts and images.

Each is fetched once however many pages name it. A chunk is read for the
chunks it loads in turn, so the lazily loaded ones -- the ones that crash the
page when missing -- come along too.
"""

from __future__ import annotations

import logging
import threading
from collections import deque
from pathlib import Path

from build.marketing_mirror import rewrite, settings
from build.marketing_mirror.fetcher import FetchError, Fetcher

LOGGER = logging.getLogger("marketing_mirror")


class AssetStore:
    def __init__(self, fetcher: Fetcher, site_dir: Path) -> None:
        self._fetcher = fetcher
        self._site_dir = site_dir
        self._lock = threading.Lock()
        self._claimed: set[str] = set()
        self.failed: set[str] = set()
        self.patches_applied: set[str] = set()

    @property
    def count(self) -> int:
        return len(self._claimed) - len(self.failed)

    def _claim(self, path: str) -> bool:
        with self._lock:
            if path in self._claimed:
                return False
            self._claimed.add(path)
            return True

    def _write(self, path: str, data: bytes) -> None:
        target = self._site_dir / path.lstrip("/")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)

    def _fetch(self, url: str, path: str) -> bytes | None:
        try:
            return self._fetcher.get(url)
        except FetchError as error:
            LOGGER.warning("asset not mirrored: %s", error)
            with self._lock:
                self.failed.add(path)
            return None

    def add_next(self, paths: set[str]) -> None:
        pending = deque(sorted(paths))
        while pending:
            path = pending.popleft()
            if not self._claim(path):
                continue
            data = self._fetch(settings.ORIGIN + path, path)
            if data is None:
                continue
            if path.endswith(".js"):
                data, applied = rewrite.patch_chunk(data)
                with self._lock:
                    self.patches_applied |= applied
            if path.endswith((".js", ".css")):
                pending.extend(
                    sorted(rewrite.next_assets(data.decode("utf-8", "replace")))
                )
            self._write(path, data)

    def add_sanity(self, cdn_paths: set[str]) -> None:
        for cdn_path in sorted(cdn_paths):
            local = settings.LOCAL_SANITY_PREFIX + cdn_path
            if not self._claim(local):
                continue
            data = self._fetch(settings.SANITY_CDN + cdn_path, local)
            if data is not None:
                self._write(local, data)
