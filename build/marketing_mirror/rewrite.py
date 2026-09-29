"""What changes between the page redis.io serves and the page this site does.

Pure functions over text: finding the assets a page or a chunk refers to, and
rewriting a page so it reads nothing from anywhere but this site.
"""

from __future__ import annotations

import re

from build.marketing_mirror import settings

_NEXT_ASSET = re.compile(r'/_next/static/[^"\'\s)\\,]+')
# Chunks a Turbopack runtime loads on demand are named without the leading
# slash, e.g. "static/immutable/chunks/0k2cvcta4v29l.js".
_LAZY_CHUNK = re.compile(r'"(static/immutable/(?:chunks|media)/[^"\\]+)"')
_CSS_URL = re.compile(r'url\(["\']?(/_next/static/[^"\')]+)')
# Either host prefix: redis.io's own, or this site's once a page is rewritten.
# A page taken from the previous run is read in the second form.
_SANITY_URL = re.compile(
    "(?:"
    + re.escape(settings.SANITY_CDN)
    + "|"
    + re.escape(settings.LOCAL_SANITY_PREFIX)
    + r')(/(?:images|files)/[^"\'\s)\\?,]+)'
)
# An image the page names only by asset id; its URL is built in the browser.
_SANITY_ASSET_ID = re.compile(
    r"image-([0-9a-f]{40})-(\d+x\d+)-(jpg|jpeg|png|webp|gif|svg)"
)
_HEAD_OPEN = re.compile(r"<head[^>]*>")


def next_assets(text: str) -> set[str]:
    """The /_next/static/ paths an HTML page, a chunk or a stylesheet refers to."""
    found = {match.rstrip("\\") for match in _NEXT_ASSET.findall(text)}
    found.update("/_next/" + lazy for lazy in _LAZY_CHUNK.findall(text))
    found.update(_CSS_URL.findall(text))
    return {path for path in found if _is_file_path(path)}


def _is_file_path(path: str) -> bool:
    """False for a directory or a template a chunk builds a path from."""
    last = path.rsplit("/", 1)[-1]
    return "." in last and not any(char in path for char in "${}")


def sanity_assets(html: str) -> set[str]:
    """The Sanity CDN paths (without query) a page shows, however it names them."""
    found = set(_SANITY_URL.findall(html))
    for digest, size, extension in _SANITY_ASSET_ID.findall(html):
        found.add(f"{settings.SANITY_PROJECT_PATH}/{digest}-{size}.{extension}")
    return found


def _tracking_tag(host: str) -> re.Pattern[str]:
    escaped = re.escape(host)
    return re.compile(
        rf'<script[^>]*src="[^"]*{escaped}[^"]*"[^>]*>\s*</script>'
        rf'|<link[^>]*href="[^"]*{escaped}[^"]*"[^>]*/?>'
    )


_TRACKING_TAGS = tuple(_tracking_tag(host) for host in settings.TRACKING_HOSTS)


def local_images(text: str) -> str:
    """Point every Sanity image URL in `text` at this site."""
    return text.replace(settings.SANITY_CDN + "/", settings.LOCAL_SANITY_PREFIX + "/")


def rewrite_page(html: str) -> str:
    """The page as this site serves it."""
    html = local_images(html)
    for tag in _TRACKING_TAGS:
        html = tag.sub("", html)
    scripts = "".join(
        f'<script src="{src}"></script>' for src in settings.INJECTED_SCRIPTS
    )
    html, injected = _HEAD_OPEN.subn(
        lambda match: match.group(0) + scripts, html, count=1
    )
    if not injected:
        raise ValueError("page has no <head>")
    return html


def patch_chunk(data: bytes) -> tuple[bytes, set[str]]:
    """A JS chunk with the patches in settings applied, and which ones it carries.

    A chunk taken from the previous run is already patched; finding the
    replacement counts as the patch applying, so a run that fetches no new
    chunk does not read as redis.io having changed its JS.
    """
    applied: set[str] = set()
    for description, pattern, replacement in settings.JS_PATCHES:
        if pattern in data:
            data = data.replace(pattern, replacement)
            applied.add(description)
        elif replacement in data:
            applied.add(description)
    return data, applied
