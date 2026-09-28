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
    assert feed.write_feed(site) == 1


def test_write_feed_writes_valid_ndjson(site):
    feed.write_feed(site)
    lines = (site / "mirror.ndjson").read_text().splitlines()
    assert json.loads(lines[0])["id"] == "blog/fastapi"
