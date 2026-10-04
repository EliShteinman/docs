"""What changes between the page redis.io serves and the page this site does.

Pure functions over text: finding the assets a page or a chunk refers to, and
rewriting a page so it reads nothing from anywhere but this site.
"""

from __future__ import annotations

import re
from html import unescape as html_unescape

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
# The scripts rewrite_page puts first in <head>, whichever list a run used.
_INJECTED_BLOCK = re.compile(
    r'(<head[^>]*>)(?:<script src="/(?:js/runtime-config\.js|_mirror/[\w.-]+\.js)">'
    r"</script>)+"
)
# An iframe as the HTML has it and as the Next.js payload does, where `<` is
# spelled \u003c and every quote is escaped once or more.
_IFRAME = re.compile(r"(?:<|\\u003c)iframe\b(.*?)(?:>|\\u003e)", re.DOTALL)
_FRAME_SRC = re.compile(r'\bsrc=\\*"([^"\\]+)')
# A video block opens its player in a modal; the payload names the player.
_VIDEO_URL = re.compile(r'\bvideoUrl\\*":\\*"([^"\\]+)')


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


def local_embeds(text: str) -> str:
    """Point every frame in settings.LOCAL_EMBEDS at this site's copy."""
    for origin, prefix in settings.LOCAL_EMBEDS.items():
        text = text.replace(origin + "/", prefix + "/")
        text = text.replace(origin.removeprefix("https:") + "/", prefix + "/")
    return text


def framed_urls(text: str) -> set[str]:
    """Every URL the page puts in a frame: its iframes, in the HTML and in the
    Next.js payload that re-renders them, and the video modals' players."""
    found = set(_VIDEO_URL.findall(text))
    for attributes in _IFRAME.findall(text):
        found.update(_FRAME_SRC.findall(attributes))
    return {html_unescape(url) for url in found}


def _is_remote(url: str) -> bool:
    return url.startswith(("http://", "https://", "//"))


def offline_players(text: str) -> str:
    """Show settings.EMBED_UNAVAILABLE in every frame that still points away
    from this site; run after local_embeds, so only the players are left."""
    for url in sorted(filter(_is_remote, framed_urls(text)), key=len, reverse=True):
        for spelling in {url, url.replace("&", "&amp;")}:
            text = _whole_url(spelling).sub(settings.EMBED_UNAVAILABLE, text)
    return text


def _whole_url(url: str) -> re.Pattern[str]:
    """`url` where it is the whole URL, not the start of a longer link. The
    payload cuts a URL at its first \\u0026, so the rest of it goes too."""
    return re.compile(re.escape(url) + r"(?:\\u0026[^\"'\s<>\\]*)*(?=[\"'\s<>\\]|$)")


def local_embed_pages(text: str) -> set[str]:
    """The pages under a settings.LOCAL_EMBEDS prefix that the page frames."""
    prefixes = tuple(prefix + "/" for prefix in settings.LOCAL_EMBEDS.values())
    return {url.split("?")[0] for url in framed_urls(text) if url.startswith(prefixes)}


def rewrite_again(html: str) -> str:
    """A page rewritten by an earlier run, rewritten by today's rules. The
    scripts an earlier run put first in <head> come out, so they are not
    loaded twice; everything else in rewrite_page leaves a rewritten page as
    it is."""
    return rewrite_page(_INJECTED_BLOCK.sub(r"\1", html, count=1))


def rewrite_page(html: str) -> str:
    """The page as this site serves it."""
    html = local_images(html)
    html = offline_players(local_embeds(html))
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
