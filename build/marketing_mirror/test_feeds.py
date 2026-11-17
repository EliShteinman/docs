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


def _named(found: list[feeds.Listing]) -> dict[str, feeds.Listing]:
    return {listing.name: listing for listing in found}


def test_listings_send_an_author_slug_wrapped_in_slashes():
    author = _named(feeds.listings(["/blog/author/itamarhaber/"]))["author/itamarhaber"]
    assert (author.endpoint, author.query) == ("author", {"slug": "/itamarhaber/"})


@pytest.mark.parametrize(
    "path", ["/blog/", "/blog/a-post/", "/blog/category/tech/", "/blog/page/2/"]
)
def test_listings_hold_only_author_pages(path):
    assert feeds.listings([path]) == []


@pytest.fixture
def author() -> feeds.Listing:
    return _named(feeds.listings(["/blog/author/ada/"]))["author/ada"]


def test_capture_starts_after_the_posts_the_page_renders(mirror, fetcher, author):
    mirror.capture(author)
    assert fetcher.queries[0]["start"] == ["21"]


def test_capture_walks_until_the_reported_total(mirror, author):
    assert mirror.capture(author) == 2


def test_capture_names_each_batch_by_its_start(mirror, tmp_path, author):
    mirror.capture(author)
    assert feeds.batch_file(tmp_path, "author/ada", 42).is_file()


def test_capture_sends_an_author_its_slug(mirror, fetcher, author):
    mirror.capture(author)
    assert fetcher.queries[0]["slug"] == ["/ada/"]


def test_capture_points_images_at_this_site(mirror, tmp_path, author):
    mirror.capture(author)
    assert "/sanity/images/" in feeds.batch_file(tmp_path, "author/ada", 21).read_text()


def test_capture_mirrors_the_images_a_batch_names(mirror, assets, author):
    mirror.capture(author)
    assert "/images/p/d/x-1x1.png" in assets.sanity


def test_capture_walks_to_an_empty_batch_when_no_total_is_given(
    tmp_path, assets, author
):
    class NoTotal(FakeFetcher):
        def get(self, url: str) -> bytes:
            body = json.loads(super().get(url))
            body.pop("totalPosts")
            return json.dumps(body).encode()

    assert feeds.FeedMirror(NoTotal(), assets, tmp_path).capture(author) == 2


def _write_batch(site, listing: str, start: int, body: str = "{}") -> None:
    feeds.batch_file(site, listing, start).parent.mkdir(parents=True, exist_ok=True)
    feeds.batch_file(site, listing, start).write_text(body)


def test_reuse_takes_every_previous_author_batch(tmp_path):
    previous, site = tmp_path / "previous", tmp_path / "site"
    _write_batch(previous, "author/ada", 21)
    _write_batch(previous, "author/bob", 21)
    assert feeds.reuse(previous, site, FakeAssets()) == 2


def test_reuse_leaves_the_retired_blog_index_batches_behind(tmp_path):
    previous, site = tmp_path / "previous", tmp_path / "site"
    _write_batch(previous, "blog", 0)
    feeds.reuse(previous, site, FakeAssets())
    assert not feeds.batch_file(site, "blog", 0).exists()


def test_reuse_keeps_each_batch_at_its_path(tmp_path):
    previous, site = tmp_path / "previous", tmp_path / "site"
    _write_batch(previous, "author/ada", 42, '{"posts": []}')
    feeds.reuse(previous, site, FakeAssets())
    assert feeds.batch_file(site, "author/ada", 42).read_text() == '{"posts": []}'


def test_reuse_keeps_the_images_a_batch_names(tmp_path):
    previous, site, assets = tmp_path / "previous", tmp_path / "site", FakeAssets()
    _write_batch(previous, "author/ada", 21, '{"src": "/sanity/images/p/d/x-1x1.png"}')
    feeds.reuse(previous, site, assets)
    assert assets.sanity == {"/images/p/d/x-1x1.png"}


def test_a_tree_with_the_blog_index_batches_is_not_complete(tmp_path):
    _write_batch(tmp_path, "author/ada", 21)
    _write_batch(tmp_path, "blog", 0)
    assert not feeds.complete(tmp_path)


def test_a_tree_with_only_author_batches_is_complete(tmp_path):
    _write_batch(tmp_path, "author/ada", 21)
    assert feeds.complete(tmp_path)
