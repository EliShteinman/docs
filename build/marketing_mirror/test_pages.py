import pytest

from build.marketing_mirror.assets import AssetStore
from build.marketing_mirror.embeds import EmbedMirror
from build.marketing_mirror.manifest import Manifest
from build.marketing_mirror.assets import replace_file
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
    embeds = EmbedMirror(fetcher, site)
    return PageMirror(fetcher, assets, embeds, site, previous_dir, previous)


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


def test_an_unchanged_page_gets_today_s_rewrite_rules(mirror, tmp_path):
    mirror.capture("/blog/a/", DATE)
    page = html_file(tmp_path / "site", "/blog/a/").read_text()
    assert page.startswith('<html><head><script src="/js/runtime-config.js">')


def test_an_unchanged_page_leaves_the_previous_run_as_it_was(mirror, previous_dir):
    mirror.capture("/blog/a/", DATE)
    assert (
        html_file(previous_dir, "/blog/a/").read_text()
        == "<html><head></head>old</html>"
    )


def test_replace_file_writes_the_new_content(tmp_path):
    target = tmp_path / "index.html"
    target.write_text("old")
    replace_file(target, b"new")
    assert target.read_bytes() == b"new"


def test_replace_file_leaves_a_hard_link_elsewhere_alone(tmp_path):
    original, linked = tmp_path / "a.html", tmp_path / "b.html"
    original.write_text("old")
    linked.hardlink_to(original)
    replace_file(linked, b"new")
    assert original.read_text() == "old"


class RedirectingFetcher(FakeFetcher):
    def get(self, url: str) -> bytes:
        if url.endswith(".md"):
            return b"<!DOCTYPE html><html><body>Partners</body></html>"
        return super().get(url)


def test_an_html_page_answering_for_markdown_is_not_saved_as_markdown(tmp_path):
    site = tmp_path / "site"
    fetcher = RedirectingFetcher()
    mirror = PageMirror(
        fetcher, AssetStore(fetcher, site), EmbedMirror(fetcher, site), site
    )
    mirror.capture("/tutorials/moved/", DATE)
    assert not markdown_file(site, "/tutorials/moved/").exists()
