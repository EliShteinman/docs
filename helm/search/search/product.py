"""Which product a page belongs to, for the modal's product dropdown.

search-modal.html offers seven products plus "all". Measured against the live
service, each one selects pages by the SECOND segment of the URL path and
ignores the first: p=redisinsight returns both /operate/redisinsight/... and
/integrate/redisinsight/..., so the leading operate / integrate / develop
segment is not part of the rule.

A page under none of the seven carries no product tag. It is still returned
for p=all, because the tag filter is only added when a specific product is
asked for.
"""

from search.paths import segments

# The `value` attributes of the <select> in search-modal.html. An unknown value
# is not rejected: the live service answers p=banana with total 0 rather than
# an error, and a TAG filter on a value nothing carries does the same here.
KNOWN_PRODUCTS = frozenset(
    {
        "rs",
        "rc",
        "oss_and_stack",
        "redisinsight",
        "kubernetes",
        "redis-data-integration",
        "clients",
    }
)

ALL_PRODUCTS = "all"


def product_of(url: str) -> str:
    """Return the product `url` belongs to, or "" when it belongs to none."""
    path_segments = segments(url)
    if len(path_segments) < 2:
        return ""
    candidate = path_segments[1]
    return candidate if candidate in KNOWN_PRODUCTS else ""
