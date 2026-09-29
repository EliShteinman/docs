"""What the previous run captured, so this run fetches only what changed.

redis.io's sitemap dates every page (`lastmod`). A page whose date has not moved
since the last run is taken from disk, not fetched; nor is any asset already
on disk, since Next.js chunks and Sanity images are named by their content.

The one change a date does not show is redis.io's frame -- the header, menus
and footer every page carries, and the chunks they load. A run fetches one
probe page every time and records the chunks it names; when they differ from
the previous run, the pages taken from disk still wear the old frame, and the
run says so. `make mirror-full` refreshes them all.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from build.marketing_mirror import settings

MANIFEST_NAME = "manifest.json"


@dataclass
class Manifest:
    pages: dict[str, str] = field(default_factory=dict)
    frame: list[str] = field(default_factory=list)

    def is_current(self, path: str, lastmod: str) -> bool:
        return bool(lastmod) and self.pages.get(path) == lastmod


def load(site_dir: Path) -> Manifest:
    try:
        data = json.loads((site_dir / MANIFEST_NAME).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return Manifest()
    return Manifest(
        pages=dict(data.get("pages", {})), frame=list(data.get("frame", []))
    )


def save(site_dir: Path, manifest: Manifest) -> None:
    document = {
        "frame": sorted(manifest.frame),
        "pages": dict(sorted(manifest.pages.items())),
    }
    (site_dir / MANIFEST_NAME).write_text(
        json.dumps(document, indent=1) + "\n", encoding="utf-8"
    )


def frame_changed(previous: Manifest, frame: list[str]) -> bool:
    return bool(previous.frame) and sorted(previous.frame) != sorted(frame)


FRAME_PROBE = settings.SECTIONS[0]
