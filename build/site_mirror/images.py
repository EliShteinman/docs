"""Bringing the blog's images inside, and rewriting posts to point at them.

Images are the bulk of the mirror -- ~2,900 files against 8.8 MB of prose -- so
they are fetched through Sanity's image pipeline as WebP rather than in their
originals. Measured over a 20-image sample: 82 KB average becomes 34 KB, which
is the difference between roughly 240 MB and 100 MB of repository and image
weight for the same pictures.

SVG is fetched untouched: re-encoding it to a raster loses the reason it is an
SVG.

GIFs are the exception that needed measuring. Sanity's own pipeline flattens
one to a single frame on every conversion tried, and the corpus's 38 GIFs are
screen recordings where the animation is the content -- 156 MB of it. Converted
locally with gif2webp instead, the animation survives and the total falls to
58 MB. Not blindly, though: five of the ten heaviest grow under conversion, one
from 2.1 MB to 4.8 MB, so each file keeps whichever of the two is smaller.
Lowering the quality does not help -- q70, q50 and q35 came out within a
percent of each other on every heavy file, because the sources are already
lossy -- so the default stays high.
"""

from __future__ import annotations

import logging
import re
import shutil
import subprocess
import urllib.request
from pathlib import Path

from build.site_mirror.sanity import DATASET, PROJECT_ID, USER_AGENT

LOGGER = logging.getLogger("site_mirror.images")

CDN_HOST = "https://cdn.sanity.io"
SITE_PATH = "/images/site-mirror"

# image-<sha1>-<width>x<height>-<extension>
_REFERENCE = re.compile(r"^image-([0-9a-f]+)-(\d+x\d+)-(\w+)$")

# Fetched byte-for-byte: the CDN cannot improve on them.
PASS_THROUGH_FORMATS = frozenset({"svg", "gif"})

# Re-encoded locally after download, keeping the animation the CDN discards.
ANIMATED_FORMATS = frozenset({"gif"})

GIF_CONVERTER = "gif2webp"
GIF_QUALITY = "70"

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


def reference_from_url(url: str) -> str:
    """Return the asset reference a CDN image URL names, or "" if it is not one.

    Markdown bodies -- the tutorials in particular -- embed images as plain CDN
    URLs rather than as references, so they arrive the other way round from the
    Portable Text ones and have to be turned back into a reference before the
    same mirroring applies.
    """
    match = re.search(
        rf"{re.escape(CDN_HOST)}/images/{PROJECT_ID}/{DATASET}/"
        r"([0-9a-f]+)-(\d+x\d+)\.(\w+)",
        url or "",
    )
    return f"image-{match.group(1)}-{match.group(2)}-{match.group(3)}" if match else ""


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
        self._converter = shutil.which(GIF_CONVERTER)
        if not self._converter:
            LOGGER.warning(
                "%s not found: animated images stay as GIFs, which costs about "
                "100 MB across the corpus",
                GIF_CONVERTER,
            )
        self.fetched = 0
        self.skipped = 0
        self.converted = 0
        self.failed: list[str] = []

    def ensure(self, reference: str) -> str:
        """Fetch the image if it is not already on disk. Returns its site path."""
        name = stored_name(reference)
        if not name:
            LOGGER.warning("unusable image reference: %s", reference)
            return ""
        destination = self._directory / name
        converted = destination.with_suffix(".webp")
        # An animated image may already be here under either name, depending on
        # whether the conversion won last time.
        for existing in (destination, converted):
            if existing.exists() and existing.stat().st_size > 0:
                self.skipped += 1
                return f"{SITE_PATH}/{existing.name}"
        try:
            self._download(source_url(reference), destination)
        except OSError as error:
            # One unreachable image must not cost the whole mirror: the post is
            # still worth having with a picture missing from it.
            LOGGER.warning("could not fetch %s: %s", reference, error)
            self.failed.append(reference)
            return ""
        self.fetched += 1
        parsed = parse_reference(reference)
        if parsed and parsed[2] in ANIMATED_FORMATS:
            destination = self._shrink_animation(destination)
        return f"{SITE_PATH}/{destination.name}"

    def ensure_url(self, url: str) -> str:
        """Mirror an image embedded in markdown as a CDN URL. Returns its site path."""
        reference = reference_from_url(url)
        return self.ensure(reference) if reference else ""

    def _shrink_animation(self, source: Path) -> Path:
        """Re-encode an animated image, keeping whichever file is smaller.

        Returns the path that should be linked. Conversion is best-effort: if
        the tool is missing or fails, the original stays and the mirror is
        larger rather than broken.
        """
        if not self._converter:
            return source
        target = source.with_suffix(".webp")
        result = subprocess.run(
            [self._converter, "-q", GIF_QUALITY, "-m", "4", "-mt", str(source), "-o", str(target)],
            capture_output=True,
        )
        if result.returncode != 0 or not target.exists() or target.stat().st_size == 0:
            LOGGER.warning("could not convert %s; keeping the original", source.name)
            target.unlink(missing_ok=True)
            return source
        if target.stat().st_size >= source.stat().st_size:
            # Conversion made it bigger, which happens on about a fifth of them.
            target.unlink()
            return source
        source.unlink()
        self.converted += 1
        return target

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
