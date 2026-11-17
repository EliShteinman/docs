import pytest

from build.marketing_mirror import listing_pages


def _links(listing: str, *numbers: int) -> str:
    return "".join(f'<a href="{listing}page/{n}/">{n}</a>' for n in numbers)


@pytest.mark.parametrize("path", ["/blog/", "/blog/category/product/"])
def test_the_blog_index_and_categories_are_listings(path):
    assert listing_pages.is_listing(path)


@pytest.mark.parametrize(
    "path", ["/blog/a-post/", "/blog/author/ada/", "/blog/page/2/", "/tutorials/"]
)
def test_other_pages_are_not_listings(path):
    assert not listing_pages.is_listing(path)


def test_numbered_pages_run_to_the_highest_page_linked():
    html = _links("/blog/", 2, 3, 5)
    assert listing_pages.numbered_pages("/blog/", html) == [
        "/blog/page/2/",
        "/blog/page/3/",
        "/blog/page/4/",
        "/blog/page/5/",
    ]


def test_a_listing_without_pagination_has_no_numbered_pages():
    assert listing_pages.numbered_pages("/blog/category/news/", "<html></html>") == []


def test_numbered_pages_ignore_another_listings_links():
    html = _links("/blog/category/product/", 2, 9)
    assert listing_pages.numbered_pages("/blog/", html) == []
