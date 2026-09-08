"""Turning a feed record's `url` into a path the rest of the package compares.

The air-gapped image builds with baseURL="/" (Dockerfile:49), so `url` in the
feed is already site-relative. A build made without that substitution carries
an absolute https://redis.io/... URL instead, and the same feed still has to
index correctly, so the scheme and host are stripped here rather than assumed
away. A deployment served under a path prefix keeps working too: every record
shares the prefix, so ancestor lookup by prefix is unaffected.
"""

_SCHEME_SEPARATOR = "://"


def to_path(url: str) -> str:
    """Return the site-relative path of `url`, without query, fragment or trailing slash."""
    path = url.strip()
    if _SCHEME_SEPARATOR in path:
        after_scheme = path.split(_SCHEME_SEPARATOR, 1)[1]
        slash = after_scheme.find("/")
        path = after_scheme[slash:] if slash != -1 else "/"
    path = path.split("#", 1)[0].split("?", 1)[0]
    if not path.startswith("/"):
        path = "/" + path
    trimmed = path.rstrip("/")
    return trimmed or "/"


def segments(url: str) -> list[str]:
    """Return the non-empty path segments of `url`, outermost first."""
    return [segment for segment in to_path(url).split("/") if segment]


def ancestors(url: str) -> list[str]:
    """Return every path from the outermost segment down to `url` itself.

    "/develop/ai/redisvl" yields ["/develop", "/develop/ai", "/develop/ai/redisvl"].
    The site root is not included: it is the caller's fixed root crumb, and it
    has no record of its own in the feed (config.toml gives the home page no
    JSON output).
    """
    trail: list[str] = []
    accumulated = ""
    for segment in segments(url):
        accumulated += "/" + segment
        trail.append(accumulated)
    return trail
