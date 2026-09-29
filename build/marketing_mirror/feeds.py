"""The blog's listings past their first screen.

The blog index and each category page render their first posts and fetch the
rest as the reader scrolls, 21 at a time, from redis.io's own API:

    /api/blog/feed?start=21&end=42&language=en
    /api/blog/category?start=21&end=42&language=en&pathname=/blog/category/tech/&slug=tech

Nothing answers those here, so every batch is captured as a file --
_feed/blog/<start>.json and _feed/category/<slug>/<start>.json -- and the
mirror pod's nginx answers each request from the file its `start` names
(runtime/nginx.conf). A listing is walked until a batch comes back empty or
the total redis.io reports is reached.

One new, removed or edited post shifts every batch after it, so the batches
are refetched whenever any page is; a run that fetches no page takes them from
the previous run instead.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from urllib.parse import urlencode

from build.marketing_mirror import rewrite, settings
from build.marketing_mirror.assets import AssetStore, place
from build.marketing_mirror.fetcher import Fetcher

LOGGER = logging.getLogger("marketing_mirror")

CATEGORY_PREFIX = "/blog/category/"


def batch_file(site_dir: Path, listing: str, start: int) -> Path:
    return site_dir / settings.FEED_DIR / listing / f"{start}.json"


def listings(page_paths: list[str]) -> dict[str, dict[str, str]]:
    """Each listing to walk: its file directory, and the query redis.io sends for it."""
    found: dict[str, dict[str, str]] = {"blog": {}}
    for path in page_paths:
        slug = path.removeprefix(CATEGORY_PREFIX).strip("/")
        if path.startswith(CATEGORY_PREFIX) and slug and "/" not in slug:
            found[f"category/{slug}"] = {"pathname": path, "slug": slug}
    return found


def reuse(previous_dir: Path, site_dir: Path, assets: AssetStore) -> int:
    """Take the previous run's batches, and the images they name. Returns how many."""
    batches = sorted((previous_dir / settings.FEED_DIR).rglob("*.json"))
    for batch in batches:
        place(batch, site_dir / batch.relative_to(previous_dir))
        assets.add_sanity(rewrite.sanity_assets(batch.read_text(encoding="utf-8")))
    return len(batches)


class FeedMirror:
    def __init__(self, fetcher: Fetcher, assets: AssetStore, site_dir: Path) -> None:
        self._fetcher = fetcher
        self._assets = assets
        self._site_dir = site_dir

    def capture_all(self, page_paths: list[str]) -> int:
        """Capture every listing's batches. Returns how many were written."""
        return sum(
            self.capture(listing, extra)
            for listing, extra in listings(page_paths).items()
        )

    def capture(self, listing: str, extra: dict[str, str]) -> int:
        endpoint = "category" if extra else "feed"
        written = 0
        start = settings.FEED_BATCH
        while True:
            query = {
                "start": str(start),
                "end": str(start + settings.FEED_BATCH),
                "language": "en",
                **extra,
            }
            url = f"{settings.ORIGIN}/api/blog/{endpoint}/?{urlencode(query)}"
            body = self._fetcher.get(url).decode("utf-8")
            batch = json.loads(body)
            posts = batch.get("posts") or []
            if not posts:
                return written
            self._assets.add_sanity(rewrite.sanity_assets(body))
            target = batch_file(self._site_dir, listing, start)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(rewrite.local_images(body), encoding="utf-8")
            written += 1
            start += settings.FEED_BATCH
            if start >= int(batch.get("totalPosts") or 0):
                return written
