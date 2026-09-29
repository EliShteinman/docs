import pytest

from build.marketing_mirror import sitemap

INDEX = b"""<?xml version="1.0"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap><loc>https://redis.io/sitemap/pages.xml</loc></sitemap>
</sitemapindex>"""

PAGES = b"""<?xml version="1.0"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://redis.io/blog/a-post/</loc><lastmod>2026-09-01T00:00:00Z</lastmod></url>
  <url><loc>https://redis.io/blog/a-post</loc></url>
  <url><loc>https://redis.io/pricing/</loc></url>
  <url><loc>https://redis.io/glossary/</loc></url>
  <url><loc>https://redis.io/glossary/acid/</loc></url>
  <url><loc>https://redis.io/es/blog/una-entrada/</loc></url>
</urlset>"""


class FakeFetcher:
    def __init__(self, responses: dict[str, bytes]) -> None:
        self.responses = responses

    def get(self, url: str) -> bytes:
        return self.responses[url]


@pytest.fixture
def paths() -> list[str]:
    fetcher = FakeFetcher(
        {
            "https://redis.io/sitemap.xml": INDEX,
            "https://redis.io/sitemap/pages.xml": PAGES,
        }
    )
    return sitemap.page_dates(fetcher)


def test_page_dates_keeps_a_mirrored_section(paths):
    assert "/blog/a-post/" in paths


def test_page_dates_keep_the_date_of_a_page_listed_twice(paths):
    assert paths["/blog/a-post/"] == "2026-09-01T00:00:00Z"


def test_page_dates_give_an_undated_page_an_empty_date(paths):
    assert paths["/glossary/acid/"] == ""


def test_page_dates_skips_a_section_that_is_not_mirrored(paths):
    assert "/pricing/" not in paths


def test_page_dates_leaves_the_glossary_index_to_the_documentation(paths):
    assert "/glossary/" not in paths


def test_page_dates_keeps_a_glossary_term(paths):
    assert "/glossary/acid/" in paths


def test_page_dates_skips_a_translation(paths):
    assert "/es/blog/una-entrada/" not in paths


def test_write_sitemap_lists_each_path(tmp_path):
    sitemap.write_sitemap(tmp_path, ["/blog/a/", "/tutorials/b/"])
    written = (tmp_path / "sitemap.xml").read_bytes()
    assert sitemap.locations(written) == ["/blog/a/", "/tutorials/b/"]
