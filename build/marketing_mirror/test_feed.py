import json

import pytest

from build.marketing_mirror import feed

MARKDOWN = (
    "# The official FastAPI Redis SDK\n\n"
    "**Authors:** A, B | **Categories:** Tech, News | **Published:** 2026-09-24 | **Updated:** 2026-09-25\n\n"
    "Body text.\n"
)
HTML = (
    '<html><head><meta name="description" content="FastAPI &amp; Redis"/></head></html>'
)


@pytest.fixture
def entry() -> dict[str, object]:
    return feed.record("/blog/fastapi/", MARKDOWN, HTML)


def test_record_id_is_the_path_without_slashes(entry):
    assert entry["id"] == "blog/fastapi"


def test_record_title_is_the_first_heading(entry):
    assert entry["title"] == "The official FastAPI Redis SDK"


def test_record_url_is_site_relative(entry):
    assert entry["url"] == "/blog/fastapi/"


def test_record_summary_is_the_unescaped_meta_description(entry):
    assert entry["summary"] == "FastAPI & Redis"


def test_record_tags_are_the_categories(entry):
    assert entry["tags"] == ["Tech", "News"]


def test_record_last_updated_prefers_updated_over_published(entry):
    assert entry["last_updated"] == "2026-09-25"


def test_record_last_updated_falls_back_to_published():
    entry = feed.record("/x/", "# X\n**Published:** 2026-01-02\n", HTML)
    assert entry["last_updated"] == "2026-01-02"


def test_record_carries_the_schema_version_the_search_service_reads(entry):
    assert entry["schema_version"] == "2"


@pytest.fixture
def site(tmp_path):
    (tmp_path / "blog" / "fastapi").mkdir(parents=True)
    (tmp_path / "blog" / "fastapi" / "index.html").write_text(HTML)
    (tmp_path / "blog" / "fastapi.md").write_text(MARKDOWN)
    (tmp_path / "blog" / "author" / "a").mkdir(parents=True)
    (tmp_path / "blog" / "author" / "a" / "index.html").write_text(HTML)
    return tmp_path


def test_write_feed_writes_one_record_per_page_with_markdown(site):
    assert feed.write_feed(site, {}) == 1


def test_write_feed_writes_valid_ndjson(site):
    feed.write_feed(site, {})
    lines = (site / "mirror.ndjson").read_text().splitlines()
    assert json.loads(lines[0])["id"] == "blog/fastapi"


SECTIONED = (
    "# Title\n\nIntro prose.\n\n"
    "## Using the SDK\n\nFirst part.\n\n```python\n## not a heading\nx = 1\n```\n\n"
    "### Caching data\n\nSecond part.\n"
)


@pytest.fixture
def split() -> list[dict[str, str]]:
    return feed.sections(SECTIONED)


def test_sections_start_with_the_prose_before_the_first_heading(split):
    assert split[0]["text"] == "# Title\n\nIntro prose."


def test_sections_split_at_second_and_third_level_headings(split):
    assert [section["title"] for section in split[1:]] == [
        "Using the SDK",
        "Caching data",
    ]


def test_sections_ignore_a_heading_inside_a_code_block(split):
    assert "not a heading" not in [section["title"] for section in split]


def test_sections_replace_code_with_the_feed_placeholder(split):
    assert split[1]["text"] == "First part.\n\n[code example]"


def test_sections_carry_an_anchor_style_id(split):
    assert split[1]["id"] == "using-the-sdk"


def test_record_carries_the_sections_the_search_service_indexes(entry):
    assert entry["sections"][0]["text"].endswith("Body text.")


STREAMED_PAGE = (
    "<html><head><title>Redis vs ElastiCache | Redis</title></head><body>"
    "<header><nav>Platform menu</nav></header><main></main><footer>Footer</footer>"
    '<div hidden id="S:0"><h1>Redis vs ElastiCache</h1><h2>Deployment</h2>'
    "<p>Any cloud.</p></div><script>swap()</script></body></html>"
)


@pytest.fixture
def html_site(tmp_path):
    (tmp_path / "compare" / "elasticache").mkdir(parents=True)
    (tmp_path / "compare" / "elasticache" / "index.html").write_text(STREAMED_PAGE)
    (tmp_path / "compare").joinpath("index.html").write_text(STREAMED_PAGE)
    return tmp_path


def test_a_page_without_markdown_gets_a_record_from_its_html(html_site):
    ids = [entry["id"] for entry in feed.records(html_site, {})]
    assert ids == ["compare/elasticache"]


def test_a_record_from_html_takes_the_page_title(html_site):
    entry = next(feed.records(html_site, {}))
    assert entry["title"] == "Redis vs ElastiCache"


def test_a_record_from_html_is_split_at_its_headings(html_site):
    entry = next(feed.records(html_site, {}))
    assert [section["title"] for section in entry["sections"]][-1] == "Deployment"


def test_a_record_from_html_takes_its_date_from_the_sitemap(html_site):
    entry = next(feed.records(html_site, {"/compare/elasticache/": "2026-09-01"}))
    assert entry["last_updated"] == "2026-09-01"


@pytest.mark.parametrize("path", ["/blog/", "/blog/category/tech/", "/blog/author/a/"])
def test_a_listing_is_not_indexed(path):
    assert feed.is_listing(path)
