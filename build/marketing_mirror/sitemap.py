"""Which pages to mirror: everything redis.io's sitemap lists under a section.

The sitemap is redis.io's own statement of what it publishes, so it covers
the pages a query per document type would miss -- a blog author's page, a
category listing -- and it drops a page the day redis.io stops serving it.
"""

from __future__ import annotations

import xml.etree.ElementTree as ElementTree
from pathlib import Path
from urllib.parse import urlsplit
from xml.sax.saxutils import escape

from build.marketing_mirror import settings
from build.marketing_mirror.fetcher import Fetcher

_NAMESPACE = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def locations(document: bytes) -> list[str]:
    """Every <loc> in a sitemap or a sitemap index."""
    root = ElementTree.fromstring(document)
    return [
        loc.text.strip() for loc in root.iterfind(".//sm:loc", _NAMESPACE) if loc.text
    ]


def is_mirrored(path: str) -> bool:
    if path in settings.EXCLUDED_PAGES:
        return False
    return any(path.startswith(section) for section in settings.SECTIONS)


def dated_locations(document: bytes) -> list[tuple[str, str]]:
    """Every (<loc>, <lastmod>) in a sitemap; the date is "" where there is none."""
    root = ElementTree.fromstring(document)
    found: list[tuple[str, str]] = []
    for url in root.iterfind("sm:url", _NAMESPACE):
        loc = url.findtext("sm:loc", default="", namespaces=_NAMESPACE).strip()
        lastmod = url.findtext("sm:lastmod", default="", namespaces=_NAMESPACE).strip()
        if loc:
            found.append((loc, lastmod))
    return found


def page_dates(
    fetcher: Fetcher, index_url: str = settings.SITEMAP_INDEX
) -> dict[str, str]:
    """Every page to mirror, by site-relative path, with the date redis.io gives it."""
    pages: dict[str, str] = {}
    for sitemap_url in locations(fetcher.get(index_url)):
        for page_url, lastmod in dated_locations(fetcher.get(sitemap_url)):
            path = urlsplit(page_url).path
            if not path.endswith("/"):
                path += "/"
            if is_mirrored(path):
                pages[path] = max(lastmod, pages.get(path, ""))
    return dict(sorted(pages.items()))


def write_sitemap(site_dir: Path, paths: list[str]) -> None:
    """The mirror's own sitemap, served by the chart at /sitemap-mirror.xml.

    Site-relative, like every URL in this image: the same image serves under
    whatever hostname a deployment gives it.
    """
    urls = "".join(f"<url><loc>{escape(path)}</loc></url>" for path in paths)
    document = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="{_NAMESPACE["sm"]}">{urls}</urlset>\n'
    (site_dir / settings.SITEMAP_NAME).write_text(document, encoding="utf-8")
