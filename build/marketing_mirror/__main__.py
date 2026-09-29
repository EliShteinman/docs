"""Mirror redis.io's marketing site into mirror/site.

    python -m build.marketing_mirror [--full] [--limit N] [--check]

A run fetches only what changed. redis.io's sitemap dates every page; a page
whose date has not moved since the last run (manifest.py) is taken from disk,
and so is every Next.js chunk and image already there, since they are named by
their content. What is taken from disk is hard-linked, not copied.

The header, menus and footer are part of every page, and a date does not move
when only they change. Each run compares the chunks one probe page loads with
the last run's and says when they differ; --full then refetches every page, so
none keeps the old frame.

The run writes a fresh directory and replaces mirror/site only when it is
complete. Run by hand, then commit the result: the image build reads
mirror/site and never reaches redis.io.
"""

from __future__ import annotations

import argparse
import logging
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from build.marketing_mirror import (
    feed,
    feeds,
    manifest,
    pages,
    rewrite,
    settings,
    sitemap,
)
from build.marketing_mirror.assets import AssetStore
from build.marketing_mirror.feeds import FeedMirror
from build.marketing_mirror.fetcher import FetchError, HttpFetcher, Moved

LOGGER = logging.getLogger("marketing_mirror")


class CaptureFailed(RuntimeError):
    """The run is not good enough to replace the mirror on disk."""


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--output", type=Path, default=settings.SITE_DIR)
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Mirror only the first N pages, for trying a change.",
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Refetch every page; assets already on disk are still reused.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Report pages redis.io lists that are not on disk.",
    )
    parser.add_argument("--workers", type=int, default=settings.WORKERS)
    parser.add_argument("--log-level", default="INFO")
    return parser.parse_args(argv)


def probe_frame(fetcher: HttpFetcher) -> list[str]:
    """The chunks redis.io's frame loads today, read off one freshly fetched page."""
    html = fetcher.get(settings.ORIGIN + manifest.FRAME_PROBE).decode("utf-8")
    return sorted(rewrite.next_assets(html))


def capture(
    dated: dict[str, str],
    staging: Path,
    workers: int,
    previous_dir: Path | None,
    previous: manifest.Manifest,
) -> manifest.Manifest:
    fetcher = HttpFetcher()
    frame = probe_frame(fetcher)
    if manifest.frame_changed(previous, frame):
        LOGGER.warning(
            "redis.io changed its header, menus or footer since the last run; "
            "pages taken from disk keep the old ones until `make mirror-full`"
        )
    assets = AssetStore(fetcher, staging, previous_dir)
    mirror = pages.PageMirror(fetcher, assets, staging, previous_dir, previous)
    paths = list(dated)
    failed: list[str] = []
    moved: list[str] = []
    fetched = 0
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(mirror.capture, path, dated[path]): path for path in paths
        }
        for done, future in enumerate(as_completed(futures), start=1):
            try:
                fetched += future.result()
            except Moved as error:
                moved.append(futures[future])
                LOGGER.info("page not mirrored, redis.io moved it: %s", error)
            except (FetchError, ValueError) as error:
                failed.append(futures[future])
                LOGGER.error("page not mirrored: %s", error)
            if done % 100 == 0:
                LOGGER.info("%d/%d pages", done, len(paths))
    unchanged = fetched == 0 and not failed and previous.pages == dated
    if unchanged and previous_dir is not None:
        batches = feeds.reuse(previous_dir, staging, assets)
        LOGGER.info("%d blog listing batches, from disk", batches)
    else:
        batches = FeedMirror(fetcher, assets, staging).capture_all(paths)
        LOGGER.info("%d blog listing batches", batches)
    _verify(paths, failed, assets)
    kept = sorted(set(paths) - set(failed) - set(moved))
    sitemap.write_sitemap(staging, kept)
    records = feed.write_feed(staging, dated)
    # The frame the pages on disk carry: the probe's only once every page
    # was fetched again, so the warning above repeats until they are.
    carried = frame if fetched == len(kept) or not previous.frame else previous.frame
    captured = manifest.Manifest(
        pages={path: dated[path] for path in kept}, frame=carried
    )
    manifest.save(staging, captured)
    LOGGER.info(
        "%d pages (%d fetched, %d from disk), %d assets (%d from disk), %d search records",
        len(kept),
        fetched,
        len(kept) - fetched,
        assets.count,
        assets.reused,
        records,
    )
    return captured


def _verify(paths: list[str], failed: list[str], assets: AssetStore) -> None:
    if len(failed) > len(paths) * settings.MAX_FAILED_SHARE:
        raise CaptureFailed(f"{len(failed)} of {len(paths)} pages failed")
    missing = {
        description for description, _, _ in settings.JS_PATCHES
    } - assets.patches_applied
    if missing:
        raise CaptureFailed(
            f"redis.io changed its JS; these patches matched nothing: {sorted(missing)}"
        )
    if assets.failed:
        LOGGER.warning("%d assets could not be mirrored", len(assets.failed))


def replace(site_dir: Path, staging: Path) -> None:
    previous = site_dir.with_name(site_dir.name + ".previous")
    shutil.rmtree(previous, ignore_errors=True)
    if site_dir.exists():
        site_dir.rename(previous)
    staging.rename(site_dir)
    shutil.rmtree(previous, ignore_errors=True)


def check(site_dir: Path) -> int:
    listed = sitemap.page_dates(HttpFetcher())
    missing = [path for path in listed if not pages.html_file(site_dir, path).is_file()]
    LOGGER.info(
        "redis.io lists %d pages; %d are not mirrored", len(listed), len(missing)
    )
    for path in missing[:20]:
        LOGGER.info("  missing: %s", path)
    return len(missing)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    logging.basicConfig(
        level=args.log_level.upper(),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    try:
        if args.check:
            check(args.output)
            return 0
        dated = sitemap.page_dates(HttpFetcher())
        if args.limit:
            dated = dict(list(dated.items())[: args.limit])
        # Assets are reused even by --full: they are named by their content,
        # so the one on disk is the one redis.io would send. --full only
        # forgets the page dates, so every page is fetched again.
        previous_dir = args.output if args.output.is_dir() else None
        previous = manifest.Manifest() if args.full else manifest.load(args.output)
        LOGGER.info("mirroring %d pages", len(dated))
        staging = args.output.with_name(args.output.name + ".staging")
        shutil.rmtree(staging, ignore_errors=True)
        capture(dated, staging, args.workers, previous_dir, previous)
        replace(args.output, staging)
    except (FetchError, CaptureFailed) as error:
        LOGGER.critical("mirror not updated: %s", error)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
