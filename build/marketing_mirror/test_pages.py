import pytest

from build.marketing_mirror.assets import AssetStore
from build.marketing_mirror.manifest import Manifest
from build.marketing_mirror.pages import PageMirror, html_file, markdown_file

DATE = "2026-09-24T22:31:58Z"
PAGE = '<html><head></head><body><img src="https://cdn.sanity.io/images/p/d/x-1x1.png"/></body></html>'


class FakeFetcher:
    def __init__(self) -> None:
        self.requested: list[str] = []

    def get(self, url: str) -> bytes:
        self.requested.append(url)
        if url.endswith(".md"):
            return b"# A post\n"
        if url.endswith(".png"):
            return b"png"
        return PAGE.encode()


@pytest.fixture
def previous_dir(tmp_path):
    previous = tmp_path / "previous"
    html_file(previous, "/blog/a/").parent.mkdir(parents=True)
    html_file(previous, "/blog/a/").write_text("<html><head></head>old</html>")
    markdown_file(previous, "/blog/a/").write_text("# old\n")
    return previous


@pytest.fixture
def fetcher() -> FakeFetcher:
    return FakeFetcher()


@pytest.fixture
def mirror(fetcher, tmp_path, previous_dir) -> PageMirror:
    site = tmp_path / "site"
    assets = AssetStore(fetcher, site, previous_dir)
    previous = Manifest(pages={"/blog/a/": DATE})
    return PageMirror(fetcher, assets, site, previous_dir, previous)


def test_an_unchanged_page_is_not_fetched(mirror, fetcher):
    mirror.capture("/blog/a/", DATE)
    assert fetcher.requested == []


def test_an_unchanged_page_is_taken_from_the_previous_run(mirror, tmp_path):
    mirror.capture("/blog/a/", DATE)
    assert "old" in html_file(tmp_path / "site", "/blog/a/").read_text()


def test_an_unchanged_page_keeps_its_markdown(mirror, tmp_path):
    mirror.capture("/blog/a/", DATE)
    assert markdown_file(tmp_path / "site", "/blog/a/").read_text() == "# old\n"


def test_an_unchanged_page_reports_it_was_not_fetched(mirror):
    assert mirror.capture("/blog/a/", DATE) is False


def test_a_page_with_a_new_date_is_fetched(mirror, fetcher):
    mirror.capture("/blog/a/", "2026-09-30T00:00:00Z")
    assert "https://redis.io/blog/a/" in fetcher.requested


def test_a_new_page_is_fetched(mirror):
    assert mirror.capture("/blog/b/", DATE) is True


def test_a_fetched_page_is_written_rewritten(mirror, tmp_path):
    mirror.capture("/blog/b/", DATE)
    assert (
        "/sanity/images/p/d/x-1x1.png"
        in html_file(tmp_path / "site", "/blog/b/").read_text()
    )
