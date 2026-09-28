"""Mirror redis.io's marketing site into mirror/site.

    python -m build.marketing_mirror [--limit N] [--check]

Every run is a full refresh. The header, the menus and the footer are part of
every page, so refreshing only the pages that changed would leave pages
captured months apart wearing different menus. A run downloads every page with
the chunks that build of redis.io serves, writes them to a fresh directory,
and replaces mirror/site only when the run is complete.

Run by hand, then commit the result. The image build reads mirror/site and
never reaches redis.io.
"""

from __future__ import annotations

import argparse
import logging
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from build.marketing_mirror import feed, pages, settings, sitemap
from build.marketing_mirror.assets import AssetStore
from build.marketing_mirror.fetcher import FetchError, HttpFetcher

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
        "--check",
        action="store_true",
        help="Report pages redis.io lists that are not on disk.",
    )
    parser.add_argument("--workers", type=int, default=settings.WORKERS)
    parser.add_argument("--log-level", default="INFO")
    return parser.parse_args(argv)


def capture(paths: list[str], staging: Path, workers: int) -> None:
    fetcher = HttpFetcher()
    assets = AssetStore(fetcher, staging)
    mirror = pages.PageMirror(fetcher, assets, staging)
    failed: list[str] = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(mirror.capture, path): path for path in paths}
        for done, future in enumerate(as_completed(futures), start=1):
            try:
                future.result()
            except (FetchError, ValueError) as error:
                failed.append(futures[future])
                LOGGER.error("page not mirrored: %s", error)
            if done % 100 == 0:
                LOGGER.info("%d/%d pages", done, len(paths))
    _verify(paths, failed, assets)
    sitemap.write_sitemap(staging, sorted(set(paths) - set(failed)))
    records = feed.write_feed(staging)
    LOGGER.info(
        "%d pages, %d assets, %d search records",
        len(paths) - len(failed),
        assets.count,
        records,
    )


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
    listed = sitemap.page_paths(HttpFetcher())
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
        paths = sitemap.page_paths(HttpFetcher())
        if args.limit:
            paths = paths[: args.limit]
        LOGGER.info("mirroring %d pages", len(paths))
        staging = args.output.with_name(args.output.name + ".staging")
        shutil.rmtree(staging, ignore_errors=True)
        capture(paths, staging, args.workers)
        replace(args.output, staging)
    except (FetchError, CaptureFailed) as error:
        LOGGER.critical("mirror not updated: %s", error)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
