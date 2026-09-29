import json
from urllib.parse import parse_qs, urlsplit

import pytest

from build.marketing_mirror import feeds

TOTAL = 50


def _batch(start: int) -> bytes:
    end = min(start + 21, TOTAL)
    posts = [{"pathname": f"/blog/post-{n}/"} for n in range(start, end)]
    image = "https://cdn.sanity.io/images/p/d/x-1x1.png"
    return json.dumps({"posts": posts, "totalPosts": TOTAL, "image": image}).encode()


class FakeFetcher:
    def __init__(self) -> None:
        self.queries: list[dict[str, list[str]]] = []

    def get(self, url: str) -> bytes:
        query = parse_qs(urlsplit(url).query)
        self.queries.append(query)
        return _batch(int(query["start"][0]))


class FakeAssets:
    def __init__(self) -> None:
        self.sanity: set[str] = set()

    def add_sanity(self, paths: set[str]) -> None:
        self.sanity |= paths


@pytest.fixture
def fetcher() -> FakeFetcher:
    return FakeFetcher()


@pytest.fixture
def assets() -> FakeAssets:
    return FakeAssets()


@pytest.fixture
def mirror(fetcher, assets, tmp_path) -> feeds.FeedMirror:
    return feeds.FeedMirror(fetcher, assets, tmp_path)


def test_listings_include_the_blog_index():
    assert feeds.listings([])["blog"] == {}


def test_listings_include_each_category_with_its_query():
    found = feeds.listings(["/blog/category/tech/"])
    assert found["category/tech"] == {
        "pathname": "/blog/category/tech/",
        "slug": "tech",
    }


def test_listings_skip_a_post():
    assert list(feeds.listings(["/blog/a-post/"])) == ["blog"]


def test_capture_starts_after_the_posts_the_page_renders(mirror, fetcher):
    mirror.capture("blog", {})
    assert fetcher.queries[0]["start"] == ["21"]


def test_capture_walks_until_the_reported_total(mirror):
    assert mirror.capture("blog", {}) == 2


def test_capture_names_each_batch_by_its_start(mirror, tmp_path):
    mirror.capture("blog", {})
    assert feeds.batch_file(tmp_path, "blog", 42).is_file()


def test_capture_sends_a_category_its_pathname_and_slug(mirror, fetcher):
    mirror.capture(
        "category/tech", {"pathname": "/blog/category/tech/", "slug": "tech"}
    )
    assert fetcher.queries[0]["slug"] == ["tech"]


def test_capture_points_images_at_this_site(mirror, tmp_path):
    mirror.capture("blog", {})
    assert "/sanity/images/" in feeds.batch_file(tmp_path, "blog", 21).read_text()


def test_capture_mirrors_the_images_a_batch_names(mirror, assets):
    mirror.capture("blog", {})
    assert "/images/p/d/x-1x1.png" in assets.sanity


def test_reuse_takes_every_previous_batch(tmp_path):
    previous, site = tmp_path / "previous", tmp_path / "site"
    for listing in ("blog", "category/tech"):
        feeds.batch_file(previous, listing, 21).parent.mkdir(parents=True)
        feeds.batch_file(previous, listing, 21).write_text("{}")
    assert feeds.reuse(previous, site, FakeAssets()) == 2


def test_reuse_keeps_each_batch_at_its_path(tmp_path):
    previous, site = tmp_path / "previous", tmp_path / "site"
    feeds.batch_file(previous, "category/tech", 42).parent.mkdir(parents=True)
    feeds.batch_file(previous, "category/tech", 42).write_text('{"posts": []}')
    feeds.reuse(previous, site, FakeAssets())
    assert feeds.batch_file(site, "category/tech", 42).read_text() == '{"posts": []}'


def test_reuse_keeps_the_images_a_batch_names(tmp_path):
    previous, site, assets = tmp_path / "previous", tmp_path / "site", FakeAssets()
    feeds.batch_file(previous, "blog", 21).parent.mkdir(parents=True)
    feeds.batch_file(previous, "blog", 21).write_text(
        '{"src": "/sanity/images/p/d/x-1x1.png"}'
    )
    feeds.reuse(previous, site, assets)
    assert assets.sanity == {"/images/p/d/x-1x1.png"}
