"""The blog's search page, /blog/search/, which redis.io renders per query.

On redis.io the blog's search box leads to /blog/search/?s=<words>, a page its
server builds for each query. Nothing builds pages here, so the mirror ships
one static page instead, answered from this site's own search service:

  * blog/search/index.html -- the blog index as captured, with its Next.js
    scripts removed and runtime/blog-search.js loaded in their place. Without
    React the page does not hydrate, so the script can own the post list: it
    reads ?s=, asks the search service for blog posts only, and draws a row
    for each by copying the page's own first row.
  * _mirror/blog-posts.json -- what a row shows beyond a title: date,
    categories and authors, for every post, taken from the listing batches
    (feeds.py captures the blog index's from 0, so they hold every post).
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from build.marketing_mirror import settings

SEARCH_PAGE = Path("blog") / "search" / "index.html"
POSTS_INDEX = Path("_mirror") / "blog-posts.json"
SEARCH_SCRIPT = "/_mirror/blog-search.js"

_SCRIPT_TAG = re.compile(r"<script\b[^>]*>.*?</script>", re.DOTALL)
_SCRIPT_PRELOAD = re.compile(r'<link\b[^>]*\bas="script"[^>]*/?>')
_ASSET_ID = re.compile(r"image-([0-9a-f]+)-(\d+x\d+)-(\w+)$")


def image_url(asset_id: str) -> str:
    """The local URL of a Sanity image named by its asset id; "" if not one."""
    match = _ASSET_ID.match(asset_id or "")
    if not match:
        return ""
    digest, size, extension = match.groups()
    return f"{settings.LOCAL_SANITY_PREFIX}{settings.SANITY_PROJECT_PATH}/{digest}-{size}.{extension}"


def _author(author: dict) -> dict[str, str]:
    name = " ".join(
        part for part in (author.get("firstName"), author.get("lastName")) if part
    )
    asset = ((author.get("image") or {}).get("asset") or {}).get("_id", "")
    return {"name": name, "image": image_url(asset)}


def post_summary(post: dict) -> dict[str, object]:
    return {
        "title": post.get("title", ""),
        "date": post.get("publishDate", ""),
        "categories": [c.get("title", "") for c in post.get("categories") or [] if c],
        "authors": [_author(a) for a in post.get("authors") or [] if a],
    }


def posts_index(site_dir: Path) -> dict[str, dict[str, object]]:
    """Every blog post the listing batches hold, by its path with a trailing slash."""
    posts: dict[str, dict[str, object]] = {}
    for batch in sorted((site_dir / settings.FEED_DIR / "blog").glob("*.json")):
        for post in json.loads(batch.read_text(encoding="utf-8")).get("posts") or []:
            path = (post.get("pathname") or "").rstrip("/") + "/"
            if path != "/":
                posts[path] = post_summary(post)
    return posts


def search_page(blog_index_html: str) -> str:
    """The blog index with Next.js taken out and the search script put in."""
    injected = {f'<script src="{src}"></script>' for src in settings.INJECTED_SCRIPTS}

    def keep_ours(match: re.Match[str]) -> str:
        return match.group(0) if match.group(0) in injected else ""

    page = _SCRIPT_TAG.sub(keep_ours, blog_index_html)
    page = _SCRIPT_PRELOAD.sub("", page)
    return page.replace(
        "</head>", f'<script src="{SEARCH_SCRIPT}" defer></script></head>', 1
    )


def write(site_dir: Path) -> int:
    """Write the search page and the posts index. Returns how many posts it knows."""
    blog_index = site_dir / "blog" / "index.html"
    if not blog_index.is_file():
        return 0
    page = site_dir / SEARCH_PAGE
    page.parent.mkdir(parents=True, exist_ok=True)
    page.write_text(
        search_page(blog_index.read_text(encoding="utf-8")), encoding="utf-8"
    )
    posts = posts_index(site_dir)
    target = site_dir / POSTS_INDEX
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(posts, ensure_ascii=False), encoding="utf-8")
    return len(posts)
