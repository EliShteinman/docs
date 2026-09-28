"""Everything this mirror knows about redis.io, in one place.

When redis.io changes how it builds its pages, this is the file that changes.
Each JS patch below is checked by the run: a pattern that no longer matches
anything fails the capture instead of shipping pages that quietly break.
"""

from __future__ import annotations

from pathlib import Path

ORIGIN = "https://redis.io"
SITEMAP_INDEX = f"{ORIGIN}/sitemap.xml"

# The sections this site serves from the mirror. Everything else on redis.io
# is either the documentation (served by this site from its own build) or not
# mirrored, and links to it are treated as leaving the site.
SECTIONS: tuple[str, ...] = (
    "/blog/",
    "/tutorials/",
    "/customers/",
    "/compare/",
    "/solutions/",
    "/technology/",
    "/glossary/",
    "/resources/architecture-diagrams/",
)

# /glossary/ itself is the documentation's glossary here: the docs are this
# site's root, and their glossary page has lived at /glossary/ all along. The
# marketing glossary's term pages are mirrored; its index is not.
EXCLUDED_PAGES: frozenset[str] = frozenset({"/glossary/"})

# Where a run writes. Kept out of content/ and static/ so Hugo never sees it.
OUTPUT_DIR = Path("mirror")
SITE_DIR = OUTPUT_DIR / "site"
FEED_NAME = "mirror.ndjson"
SITEMAP_NAME = "sitemap.xml"

SANITY_CDN = "https://cdn.sanity.io"
LOCAL_SANITY_PREFIX = "/sanity"
SANITY_PROJECT_PATH = "/images/sy1jschh/production"

USER_AGENT = "redis-docs-airgap-marketing-mirror/1.0"
TIMEOUT_SECONDS = 60.0
RETRIES = 3
WORKERS = 16

# A run that loses more than this share of its pages keeps the previous mirror.
MAX_FAILED_SHARE = 0.02

# Tags redis.io puts in the page for third parties. The pages load several of
# these again from their own JS, which is why the site also serves them under a
# same-origin Content-Security-Policy; removing the tags keeps the HTML honest.
TRACKING_HOSTS: tuple[str, ...] = (
    "googletagmanager.com",
    "trustarc.com",
    "consent.",
    "segment.com",
    "amplitude.com",
)

# The scripts every mirrored page loads first: the site's runtime config (the
# external-links switch) and the handler that applies it to the page.
INJECTED_SCRIPTS: tuple[str, ...] = (
    "/js/runtime-config.js",
    "/_mirror/marketing-links.js",
)

# (description, pattern, replacement) applied to every JS chunk.
JS_PATCHES: tuple[tuple[str, bytes, bytes], ...] = (
    (
        "next/image: load images directly, there is no optimizer server here",
        b'path:"/_next/image/",loader:"default",dangerouslyAllowSVG:!1,unoptimized:!1',
        b'path:"/_next/image/",loader:"default",dangerouslyAllowSVG:!1,unoptimized:!0',
    ),
    (
        "Sanity image builder: default base URL",
        b'"https://cdn.sanity.io"',
        b'"/sanity"',
    ),
    (
        "Sanity image builder: base URL derived from the client's API host",
        b'.replace(/^https:\\/\\/api\\./,"https://cdn.")',
        b'.replace(/^https:\\/\\/api\\.sanity\\.io/,"/sanity")',
    ),
)
