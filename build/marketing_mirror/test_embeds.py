import pytest

from build.marketing_mirror import settings
from build.marketing_mirror.embeds import (
    EmbedMirror,
    origin_url,
    strip_imports,
    vendor_path,
)
from build.marketing_mirror.fetcher import FetchError

ORIGIN = "https://vecsim-benchmarks-charts.s3.us-east-2.amazonaws.com"
PREFIX = "/_mirror/embeds/vecsim-benchmarks-charts"
CHART_PAGE = (
    b'<link href="./main.css" rel="stylesheet">'
    b'<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>'
    b'<script src="./benchmark.js"></script>'
    b'<a href="#top">top</a>'
    b"<script>let url = './results.json'; fetch(url)</script>"
)
STYLESHEET = (
    b'@import"https://fonts.googleapis.com/css?family=Open+Sans";'
    b'@import"flaticon.css";.content{padding:1px}'
)


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
            f"{ORIGIN}/blog/chart.html": CHART_PAGE,
            f"{ORIGIN}/blog/main.css": STYLESHEET,
            f"{ORIGIN}/blog/benchmark.js": b"draw()",
            f"{ORIGIN}/blog/results.json": b"[]",
            "https://cdn.jsdelivr.net/npm/chart.js": b"Chart",
        }
    )


@pytest.fixture
def site(fetcher, tmp_path):
    EmbedMirror(fetcher, tmp_path).add({f"{PREFIX}/blog/chart.html"})
    return tmp_path


def test_origin_url_maps_a_local_page_back_to_its_host():
    assert origin_url(f"{PREFIX}/blog/chart.html") == f"{ORIGIN}/blog/chart.html"


def test_origin_url_rejects_a_path_outside_every_prefix():
    with pytest.raises(ValueError):
        origin_url("/_mirror/other/x.html")


@pytest.mark.parametrize(
    "url", ["https://cdn.jsdelivr.net/npm/chart.js", "//cdn.jsdelivr.net/npm/chart.js"]
)
def test_vendor_path_keeps_a_cdn_file_under_its_host(url):
    expected = f"{settings.EMBED_VENDOR_PREFIX}/cdn.jsdelivr.net/npm/chart.js"
    assert vendor_path(url) == expected


def test_strip_imports_drops_every_import():
    assert strip_imports(STYLESHEET.decode()) == ".content{padding:1px}"


def test_add_writes_the_chart_page(site):
    assert (site / PREFIX.lstrip("/") / "blog/chart.html").is_file()


def test_add_loads_the_cdn_library_from_this_site(site):
    page = (site / PREFIX.lstrip("/") / "blog/chart.html").read_text()
    assert f'src="{settings.EMBED_VENDOR_PREFIX}/cdn.jsdelivr.net/npm/chart.js"' in page


def test_add_writes_the_cdn_library(site):
    vendored = site / settings.EMBED_VENDOR_PREFIX.lstrip("/") / "cdn.jsdelivr.net/npm"
    assert (vendored / "chart.js").read_bytes() == b"Chart"


def test_add_writes_a_file_next_to_the_page(site):
    assert (site / PREFIX.lstrip("/") / "blog/benchmark.js").read_bytes() == b"draw()"


def test_add_writes_the_data_an_inline_script_fetches(site):
    assert (site / PREFIX.lstrip("/") / "blog/results.json").read_bytes() == b"[]"


def test_add_writes_the_stylesheet_without_imports(site):
    stylesheet = (site / PREFIX.lstrip("/") / "blog/main.css").read_text()
    assert stylesheet == ".content{padding:1px}"


def test_add_skips_an_anchor(fetcher, site):
    assert not any("#" in url for url in fetcher.requested)


def test_add_fetches_a_page_framed_twice_once(fetcher, tmp_path):
    embeds = EmbedMirror(fetcher, tmp_path)
    embeds.add({f"{PREFIX}/blog/chart.html"})
    embeds.add({f"{PREFIX}/blog/chart.html"})
    assert fetcher.requested.count(f"{ORIGIN}/blog/chart.html") == 1


def test_add_reports_a_page_it_could_not_fetch(fetcher, tmp_path):
    embeds = EmbedMirror(fetcher, tmp_path)
    embeds.add({f"{PREFIX}/blog/gone.html"})
    assert embeds.failed == {f"{PREFIX}/blog/gone.html"}


def test_write_unavailable_page_puts_it_where_the_frames_point(fetcher, tmp_path):
    EmbedMirror(fetcher, tmp_path).write_unavailable_page()
    assert (tmp_path / settings.EMBED_UNAVAILABLE.lstrip("/")).is_file()
