"""The files the pages load: Next.js chunks, stylesheets, fonts and images.

Each is obtained once however many pages name it, and never fetched again
once a run has it: Next.js chunks and Sanity images are named by their
content, so a file already in the previous run's tree is the same file. It is
hard-linked into the new tree instead. A chunk is read for the chunks it loads
in turn, so the lazily loaded ones -- the ones that crash the page when
missing -- come along too.
"""

from __future__ import annotations

import logging
import os
import shutil
import threading
from collections import deque
from pathlib import Path

from build.marketing_mirror import rewrite, settings
from build.marketing_mirror.fetcher import FetchError, Fetcher

LOGGER = logging.getLogger("marketing_mirror")


def place(source: Path, target: Path) -> None:
    """Put `source` at `target` without copying its bytes when the disk allows."""
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.link(source, target)
    except OSError:
        shutil.copyfile(source, target)


class AssetStore:
    def __init__(
        self, fetcher: Fetcher, site_dir: Path, previous_dir: Path | None = None
    ) -> None:
        self._fetcher = fetcher
        self._site_dir = site_dir
        self._previous_dir = previous_dir
        self._lock = threading.Lock()
        self._claimed: set[str] = set()
        self.failed: set[str] = set()
        self.reused = 0
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

    def _target(self, path: str) -> Path:
        return self._site_dir / path.lstrip("/")

    def _reuse(self, path: str) -> bytes | None:
        if self._previous_dir is None:
            return None
        source = self._previous_dir / path.lstrip("/")
        if not source.is_file():
            return None
        place(source, self._target(path))
        with self._lock:
            self.reused += 1
        return source.read_bytes() if path.endswith((".js", ".css")) else b""

    def _fetch(self, url: str, path: str) -> bytes | None:
        try:
            return self._fetcher.get(url)
        except FetchError as error:
            LOGGER.warning("asset not mirrored: %s", error)
            with self._lock:
                self.failed.add(path)
            return None

    def _write(self, path: str, data: bytes) -> None:
        target = self._target(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)

    def add_next(self, paths: set[str]) -> None:
        pending = deque(sorted(paths))
        while pending:
            path = pending.popleft()
            if not self._claim(path):
                continue
            data = self._reuse(path)
            fetched = data is None
            if fetched:
                data = self._fetch(settings.ORIGIN + path, path)
                if data is None:
                    continue
            if path.endswith(".js"):
                data, applied = rewrite.patch_chunk(data)
                with self._lock:
                    self.patches_applied |= applied
            if path.endswith((".js", ".css")):
                text = data.decode("utf-8", "replace")
                pending.extend(sorted(rewrite.next_assets(text)))
            if fetched:
                self._write(path, data)

    def add_sanity(self, cdn_paths: set[str]) -> None:
        for cdn_path in sorted(cdn_paths):
            local = settings.LOCAL_SANITY_PREFIX + cdn_path
            if not self._claim(local):
                continue
            if self._reuse(local) is not None:
                continue
            data = self._fetch(settings.SANITY_CDN + cdn_path, local)
            if data is not None:
                self._write(local, data)
