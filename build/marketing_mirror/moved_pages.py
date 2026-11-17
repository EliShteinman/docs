"""Pages redis.io moved, answered here the way redis.io answers them.

redis.io redirects a page it moved, and other pages still link to the old
address. The mirror keeps no page under it (fetcher.Moved), so where the new
address is mirrored too, the old one gets a page that sends the reader there.
It is a plain HTML refresh, so it needs nothing of nginx and carries no <main>,
which keeps it out of the search feed (feed.py).
"""

from __future__ import annotations

from html import escape
from pathlib import Path

from build.marketing_mirror import pages


def with_slash(path: str) -> str:
    return path if path.endswith("/") else path + "/"


def redirect_page(target: str) -> str:
    href = escape(target, quote=True)
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        f'<meta http-equiv="refresh" content="0; url={href}">'
        f'<link rel="canonical" href="{href}"><title>Moved</title></head>'
        f'<body><p>This page moved to <a href="{href}">{href}</a>.</p></body></html>'
    )


def write(site_dir: Path, moved: dict[str, str], kept: set[str]) -> int:
    """Write a page at each moved path whose new path is mirrored. Returns how many."""
    written = 0
    for path, target in sorted(moved.items()):
        local = with_slash(target)
        if local not in kept:
            continue
        page = pages.html_file(site_dir, path)
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text(redirect_page(local), encoding="utf-8")
        written += 1
    return written
