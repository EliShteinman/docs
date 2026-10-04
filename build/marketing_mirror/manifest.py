"""What the previous run captured, so this run fetches only what changed.

redis.io's sitemap dates every page (`lastmod`). A page whose date has not moved
since the last run is taken from disk, not fetched; nor is any asset already
on disk, since Next.js chunks and Sanity images are named by their content.

A change a date does not show -- redis.io's header and footer, which every page
carries -- needs no refetch: the pages show the documentation's header and
footer instead (runtime/docs-frame.js).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


MANIFEST_NAME = "manifest.json"


@dataclass
class Manifest:
    pages: dict[str, str] = field(default_factory=dict)

    def is_current(self, path: str, lastmod: str) -> bool:
        return bool(lastmod) and self.pages.get(path) == lastmod


def load(site_dir: Path) -> Manifest:
    try:
        data = json.loads((site_dir / MANIFEST_NAME).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return Manifest()
    return Manifest(pages=dict(data.get("pages", {})))


def save(site_dir: Path, manifest: Manifest) -> None:
    document = {"pages": dict(sorted(manifest.pages.items()))}
    (site_dir / MANIFEST_NAME).write_text(
        json.dumps(document, indent=1) + "\n", encoding="utf-8"
    )
