"""Rebuilding the breadcrumb trail the live service returns as `hierarchy`.

redis.io answers with the full trail from the site root down to the page:

    ["Welcome to Redis Docs", "Develop with Redis", "Redis for AI and search",
     "RedisVL", "Concepts", "Utilities"]

search-modal.html reads [0] as the group heading and renders [1] -> [2] as the
row's path, so the trail has to start at the root -- starting at the page's own
section would put the wrong two labels in every row.

Every ancestor is itself a page in the feed, so the trail is a lookup of each
URL prefix's title. Checked against the live response for
/develop/ai/redisvl/concepts/utilities: identical apart from the root label,
which has no record of its own (config.toml gives the home page no JSON
output) and is supplied by the caller.
"""

from collections.abc import Iterable

from search.paths import ancestors, to_path


class BreadcrumbIndex:
    """Maps a page URL to its breadcrumb trail, using the titles of its ancestors."""

    def __init__(self, root_crumb: str, titles: dict[str, str]) -> None:
        self._root_crumb = root_crumb
        self._titles = titles

    @classmethod
    def from_documents(cls, root_crumb: str, documents: Iterable) -> "BreadcrumbIndex":
        return cls(root_crumb, {document.url: document.title for document in documents})

    def crumbs_for(self, url: str) -> list[str]:
        """Return the breadcrumb trail for `url`, root first and the page itself last.

        A path segment with no page of its own -- a directory that never got an
        _index -- contributes nothing. Its level is skipped rather than filled
        with a placeholder: a gap shifts the row's two labels by one, which is
        wrong, but a placeholder is wrong and also visible.
        """
        trail = [self._root_crumb]
        for ancestor in ancestors(to_path(url)):
            title = self._titles.get(ancestor)
            if title:
                trail.append(title)
        return trail
