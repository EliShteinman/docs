import pytest

from build.marketing_mirror.assets import AssetStore
from build.marketing_mirror.fetcher import FetchError

ROOT_CHUNK = b'Promise.all(["static/immutable/chunks/lazy.js"].map(t=>e.l(t)))'
LAZY_CHUNK = (
    b'path:"/_next/image/",loader:"default",dangerouslyAllowSVG:!1,unoptimized:!1'
)
STYLESHEET = b"@font-face{src:url(/_next/static/immutable/media/f.woff2)}"


class FakeFetcher:
    def __init__(self, responses: dict[str, bytes]) -> None:
        self.responses = responses
        self.requested: list[str] = []

    def get(self, url: str) -> bytes:
        self.requested.append(url)
        if url not in self.responses:
            raise FetchError(f"{url}: HTTP 404")
        return self.responses[url]


@pytest.fixture
def fetcher() -> FakeFetcher:
    return FakeFetcher(
        {
            "https://redis.io/_next/static/immutable/chunks/root.js": ROOT_CHUNK,
            "https://redis.io/_next/static/immutable/chunks/lazy.js": LAZY_CHUNK,
            "https://redis.io/_next/static/immutable/chunks/a.css": STYLESHEET,
            "https://redis.io/_next/static/immutable/media/f.woff2": b"font",
            "https://cdn.sanity.io/images/p/d/x-1x1.png": b"png",
        }
    )


@pytest.fixture
def store(fetcher, tmp_path) -> AssetStore:
    return AssetStore(fetcher, tmp_path)


def test_add_next_follows_a_lazily_loaded_chunk(store, tmp_path):
    store.add_next({"/_next/static/immutable/chunks/root.js"})
    assert (tmp_path / "_next/static/immutable/chunks/lazy.js").is_file()


def test_add_next_follows_a_font_in_a_stylesheet(store, tmp_path):
    store.add_next({"/_next/static/immutable/chunks/a.css"})
    assert (tmp_path / "_next/static/immutable/media/f.woff2").read_bytes() == b"font"


def test_add_next_patches_a_chunk_on_the_way_to_disk(store, tmp_path):
    store.add_next({"/_next/static/immutable/chunks/lazy.js"})
    assert (
        b"unoptimized:!0"
        in (tmp_path / "_next/static/immutable/chunks/lazy.js").read_bytes()
    )


def test_add_next_records_which_patch_matched(store):
    store.add_next({"/_next/static/immutable/chunks/lazy.js"})
    assert len(store.patches_applied) == 1


def test_add_next_fetches_an_asset_once(store, fetcher):
    store.add_next({"/_next/static/immutable/chunks/a.css"})
    store.add_next({"/_next/static/immutable/chunks/a.css"})
    assert (
        fetcher.requested.count("https://redis.io/_next/static/immutable/chunks/a.css")
        == 1
    )


def test_add_next_records_an_asset_it_could_not_fetch(store):
    store.add_next({"/_next/static/immutable/chunks/gone.js"})
    assert store.failed == {"/_next/static/immutable/chunks/gone.js"}


def test_add_sanity_writes_under_the_local_prefix(store, tmp_path):
    store.add_sanity({"/images/p/d/x-1x1.png"})
    assert (tmp_path / "sanity/images/p/d/x-1x1.png").read_bytes() == b"png"
