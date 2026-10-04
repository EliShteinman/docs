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
# The blog's listing batches (feeds.py), and how many posts redis.io sends per batch.
FEED_DIR = "_feed"
FEED_BATCH = 21
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
    "cloudflareinsights.com",
)

# Third parties redis.io's layout renders as React elements in every page's
# Next.js payload, by key: analytics, consent and ad pixels. They render
# nothing on the server, so taking them out of the payload changes nothing
# the page hydrates against, and nothing tries to reach them.
TRACKING_ELEMENTS: tuple[str, ...] = (
    "gtm",
    "segment-analytics",
    "amplitude-engagement",
    "trustarc",
    "fb_script",
    "qp_script",
    "twq_script",
    "spdt",
)

# Pages redis.io frames from elsewhere that are plain static files: captured
# with what they load (embeds.py) and served from this site under the prefix.
LOCAL_EMBEDS: dict[str, str] = {
    "https://vecsim-benchmarks-charts.s3.us-east-2.amazonaws.com": (
        "/_mirror/embeds/vecsim-benchmarks-charts"
    ),
}
# Where a framed file from anywhere else -- a CDN library -- is kept.
EMBED_VENDOR_PREFIX = "/_mirror/embeds/_vendor"

# Every other frame is a player (video, podcast, slides) whose media streams
# from a service this network cannot reach. It shows this page instead.
EMBED_UNAVAILABLE = "/_mirror/embed-unavailable.html"
EMBED_UNAVAILABLE_SOURCE = Path(__file__).with_name("embed-unavailable.html")

# The scripts every mirrored page loads first: the site's runtime config (the
# external-links switch), the handler that applies it to the page, and the
# documentation's header in place of redis.io's.
INJECTED_SCRIPTS: tuple[str, ...] = (
    "/js/runtime-config.js",
    "/_mirror/marketing-links.js",
    "/_mirror/docs-frame.js",
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
    (
        "video player: a player it cannot show says why, readably",
        b'{children:"Unsupported video platform or invalid URL"}',
        b'{style:{color:"#fff",padding:"16px",textAlign:"center",fontFamily:"system-ui,sans-serif"},'
        b'children:"This embedded media is hosted outside this network. '
        b'It is not available on this site."}',
    ),
    (
        "account API: asks this site, which answers 404, read as not logged in",
        b'"https://cloud.redis.io/api/v1"',
        b'"/_mirror/no-cloud-api"',
    ),
    (
        "account API: plan prices, from this site too",
        b"`https://cloud.redis.io/api/v1/accounts",
        b"`/_mirror/no-cloud-api/accounts",
    ),
    (
        "visitor IP lookup: an empty answer, without asking ipify",
        b'fetch("https://api.ipify.org?format=json")',
        b'Promise.resolve({ok:!0,json:()=>({ip:""})})',
    ),
)
