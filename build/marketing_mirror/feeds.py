"""The blog's author pages past their first screen.

An author page renders its first posts and fetches the rest as the reader
scrolls, 21 at a time, from redis.io's own API:

    /api/blog/author?start=21&end=42&slug=/<author>/

Nothing answers that here, so every batch is captured as a file --
_feed/author/<slug>/<start>.json -- and the mirror pod's nginx answers each
request from the file its `start` names (runtime/nginx.conf). A listing is
walked until a batch comes back empty or the total redis.io reports is reached.

The blog index and the category pages are numbered pages instead, each one a
page of its own (listing_pages.py).

One new, removed or edited post shifts every batch after it, so the batches
are refetched whenever any page is; a run that fetches no page takes them from
the previous run instead.
"""

from __future__ import annotations

import json
import logging
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlencode

from build.marketing_mirror import rewrite, settings
from build.marketing_mirror.assets import AssetStore, place
from build.marketing_mirror.fetcher import Fetcher

LOGGER = logging.getLogger("marketing_mirror")

AUTHOR_PREFIX = "/blog/author/"


@dataclass(frozen=True)
class Listing:
    name: str
    endpoint: str
    query: dict[str, str]


def batch_file(site_dir: Path, listing: str, start: int) -> Path:
    return site_dir / settings.FEED_DIR / listing / f"{start}.json"


def _slug(path: str, prefix: str) -> str:
    slug = path.removeprefix(prefix).strip("/")
    return slug if path.startswith(prefix) and slug and "/" not in slug else ""


def listings(page_paths: list[str]) -> list[Listing]:
    """Each author listing to walk: where its files go, and the query redis.io sends for it."""
    # The author page sends its slug wrapped in slashes, and the API answers
    # nothing for the bare one.
    return [
        Listing(f"author/{slug}", "author", {"slug": f"/{slug}/"})
        for path in page_paths
        if (slug := _slug(path, AUTHOR_PREFIX))
    ]


def _batches(site_dir: Path) -> list[Path]:
    return sorted((site_dir / settings.FEED_DIR / "author").rglob("*.json"))


def complete(site_dir: Path) -> bool:
    """Whether a tree's batches were captured the way this module captures them now.

    A tree with the blog index's batches predates the numbered listing pages;
    its author batches are refetched rather than carried on.
    """
    feed_dir = site_dir / settings.FEED_DIR
    return (feed_dir / "author").is_dir() and not (feed_dir / "blog").exists()


def reuse(previous_dir: Path, site_dir: Path, assets: AssetStore) -> int:
    """Take the previous run's batches, and the images they name. Returns how many."""
    batches = _batches(previous_dir)
    for batch in batches:
        place(batch, site_dir / batch.relative_to(previous_dir))
        assets.add_sanity(rewrite.sanity_assets(batch.read_text(encoding="utf-8")))
    return len(batches)


class FeedMirror:
    def __init__(self, fetcher: Fetcher, assets: AssetStore, site_dir: Path) -> None:
        self._fetcher = fetcher
        self._assets = assets
        self._site_dir = site_dir

    def capture_all(
        self, page_paths: list[str], workers: int = settings.WORKERS
    ) -> int:
        """Capture every listing's batches, several listings at once.

        Returns how many batches were written. A listing's own batches stay in
        order -- each needs the one before it to know where to stop -- but the
        listings do not depend on each other.
        """
        with ThreadPoolExecutor(max_workers=workers) as pool:
            return sum(pool.map(self.capture, listings(page_paths)))

    def capture(self, listing: Listing) -> int:
        written = 0
        start = settings.FEED_BATCH
        while True:
            query = {
                "start": str(start),
                "end": str(start + settings.FEED_BATCH),
                **listing.query,
            }
            url = f"{settings.ORIGIN}/api/blog/{listing.endpoint}/?{urlencode(query)}"
            body = self._fetcher.get(url).decode("utf-8")
            batch = json.loads(body)
            posts = batch.get("posts") or []
            if not posts:
                return written
            self._assets.add_sanity(rewrite.sanity_assets(body))
            target = batch_file(self._site_dir, listing.name, start)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(rewrite.local_images(body), encoding="utf-8")
            written += 1
            start += settings.FEED_BATCH
            total = batch.get("totalPosts")
            if total is not None and start >= int(total):
                return written
