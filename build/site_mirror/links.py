"""Pointing the blog's own cross-references at the mirrored copy.

Posts link to each other constantly, and they do it by absolute URL. Left
alone, a reader inside the air gap who follows one of those lands on
redis.io -- from a post that is sitting on the same server they are already
reading.

Only blog-to-blog links are rewritten here, because those are the ones the
mirror can guarantee: every post in the source is mirrored, so every such link
resolves. Links to the documentation, to GitHub, or anywhere else are left as
they are and handled at runtime by the chart's external-link machinery, which
is where per-deployment decisions about them belong.

The source spells its own blog four ways -- redis.io, the legacy redis.com and
redislabs.com domains, and a /en/ locale prefix -- and 99 of the 184 blog links
in the documentation use the legacy spellings, so matching only redis.io would
miss more than half of them.
"""

from __future__ import annotations

import re

LOCAL_SECTION = "/blog"

# Matches the blog root on any of the domains the corpus uses, with or without
# the locale prefix, and captures whatever path follows.
_BLOG_URL = re.compile(
    r"^https?://(?:www\.)?(?:redis\.io|redis\.com|redislabs\.com)(?:/en)?/blog(?P<rest>/.*)?$",
    re.IGNORECASE,
)


def localize(url: str) -> str:
    """Return the local path for a blog URL, or `url` unchanged if it is not one."""
    match = _BLOG_URL.match((url or "").strip())
    if not match:
        return url
    rest = match.group("rest") or "/"
    # Hugo publishes each post as a directory, so the trailing slash is kept:
    # without it nginx answers a redirect before serving the page.
    if not rest.endswith("/") and "#" not in rest and "?" not in rest:
        rest += "/"
    return LOCAL_SECTION + rest
