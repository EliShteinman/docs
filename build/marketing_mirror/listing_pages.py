"""The blog's numbered listing pages: /blog/page/<n>/ and /blog/category/<slug>/page/<n>/.

redis.io renders the blog index and each category 21 posts at a time, one page
per batch, and links them from the first page's pagination. The sitemap lists
only the first page, so the rest are found from its links: the highest number
a first page links to is how many pages its listing has.

Every new post shifts every page after it, and the sitemap dates none of them,
so they are fetched on every run.
"""

from __future__ import annotations

import re

from build.marketing_mirror import settings

_CATEGORY = re.compile(r"^/blog/category/[a-z0-9-]+/$")


def is_listing(path: str) -> bool:
    """Whether redis.io splits this page into numbered pages."""
    return path == settings.BLOG_INDEX or bool(_CATEGORY.match(path))


def numbered_pages(listing: str, html: str) -> list[str]:
    """The paths of a listing's pages after its first, as its first page links them."""
    link = re.compile(rf'href="{re.escape(listing)}page/(\d+)/"')
    numbers = [int(number) for number in link.findall(html)]
    last = max(numbers, default=1)
    return [f"{listing}page/{number}/" for number in range(2, last + 1)]
