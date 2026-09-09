"""Bringing the blog's images inside, and rewriting posts to point at them.

Images are the bulk of the mirror -- ~2,900 files against 8.8 MB of prose -- so
they are fetched through Sanity's image pipeline as WebP rather than in their
originals. Measured over a 20-image sample: 82 KB average becomes 34 KB, which
is the difference between roughly 240 MB and 100 MB of repository and image
weight for the same pictures.

Two formats are fetched untouched. SVG is already small and re-encoding it to a
raster loses the reason it is an SVG, and a GIF re-encoded to still WebP loses
its animation -- several of the blog's GIFs are screen recordings.
"""

from __future__ import annotations

import logging
import re
import urllib.request
from pathlib import Path

from build.blog_mirror.sanity import DATASET, PROJECT_ID, USER_AGENT

LOGGER = logging.getLogger("blog_mirror.images")

CDN_HOST = "https://cdn.sanity.io"
SITE_PATH = "/images/blog"

# image-<sha1>-<width>x<height>-<extension>
_REFERENCE = re.compile(r"^image-([0-9a-f]+)-(\d+x\d+)-(\w+)$")

PASS_THROUGH_FORMATS = frozenset({"svg", "gif"})

# Wider than the docs content column at any zoom, so a reader never sees a
# picture upscaled, without carrying originals that can be 4000px wide.
TARGET_WIDTH = 1600
WEBP_QUALITY = 80


class ImageError(RuntimeError):
    """An image could not be fetched."""


def parse_reference(reference: str) -> tuple[str, str, str] | None:
    """Split an asset reference into (digest, dimensions, extension)."""
    match = _REFERENCE.match(reference or "")
    return (match.group(1), match.group(2), match.group(3)) if match else None


def stored_name(reference: str) -> str:
    """Return the file name this reference is stored under, or "" if unusable."""
    parsed = parse_reference(reference)
    if not parsed:
        return ""
    digest, dimensions, extension = parsed
    suffix = extension if extension in PASS_THROUGH_FORMATS else "webp"
    return f"{digest}-{dimensions}.{suffix}"


def site_path(reference: str) -> str:
    """Return the path a mirrored post links the image by."""
    name = stored_name(reference)
    return f"{SITE_PATH}/{name}" if name else ""


def source_url(reference: str) -> str:
    """Return the CDN URL to fetch this reference from."""
    parsed = parse_reference(reference)
    if not parsed:
        return ""
    digest, dimensions, extension = parsed
    url = f"{CDN_HOST}/images/{PROJECT_ID}/{DATASET}/{digest}-{dimensions}.{extension}"
    if extension in PASS_THROUGH_FORMATS:
        return url
    return f"{url}?w={TARGET_WIDTH}&fm=webp&q={WEBP_QUALITY}"


class ImageMirror:
    """Downloads each referenced image once, into a directory of files."""

    def __init__(self, directory: Path, timeout: float = 60.0) -> None:
        self._directory = directory
        self._timeout = timeout
        self.fetched = 0
        self.skipped = 0
        self.failed: list[str] = []

    def ensure(self, reference: str) -> str:
        """Fetch the image if it is not already on disk. Returns its site path."""
        name = stored_name(reference)
        if not name:
            LOGGER.warning("unusable image reference: %s", reference)
            return ""
        destination = self._directory / name
        if destination.exists() and destination.stat().st_size > 0:
            self.skipped += 1
            return site_path(reference)
        try:
            self._download(source_url(reference), destination)
        except OSError as error:
            # One unreachable image must not cost the whole mirror: the post is
            # still worth having with a picture missing from it.
            LOGGER.warning("could not fetch %s: %s", reference, error)
            self.failed.append(reference)
            return ""
        self.fetched += 1
        return site_path(reference)

    def _download(self, url: str, destination: Path) -> None:
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(request, timeout=self._timeout) as response:
            payload = response.read()
        if not payload:
            raise OSError("empty response")
        destination.parent.mkdir(parents=True, exist_ok=True)
        # Written under a temporary name and moved into place, so an interrupted
        # run cannot leave a truncated file that the next run then skips.
        temporary = destination.with_suffix(destination.suffix + ".part")
        temporary.write_bytes(payload)
        temporary.replace(destination)
