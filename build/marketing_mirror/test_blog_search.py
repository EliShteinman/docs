import json

import pytest

from build.marketing_mirror import blog_search

POST = {
    "_createdAt": "2026-09-22T10:00:00Z",
    "pathname": "/blog/a-post",
    "title": "A post",
    "publishDate": "2026-09-23",
    "categories": [{"title": "Tech"}],
    "authors": [
        {
            "firstName": "Ada",
            "lastName": "Lovelace",
            "image": {"asset": {"_id": "image-" + "a" * 40 + "-800x800-jpg"}},
        }
    ],
}
INDEX = (
    '<html><head><script src="/js/runtime-config.js"></script>'
    '<link rel="preload" href="/_next/static/immutable/chunks/a.js" as="script"/>'
    '<script src="/_next/static/immutable/chunks/a.js" async=""></script>'
    "</head><body><main>list</main><script>self.__next_f.push([1])</script></body></html>"
)


def _pushes(*posts: dict) -> str:
    """A Next.js payload carrying the posts, split over two pushes."""
    payload = '1:["$","div",null,{"posts":' + json.dumps(list(posts)) + "}]"
    middle = len(payload) // 2
    return "".join(
        f"<script>self.__next_f.push([1,{json.dumps(part)}])</script>"
        for part in (payload[:middle], payload[middle:])
    )


def _listing_page(*posts: dict) -> str:
    return f"<html><head></head><body>{_pushes(*posts)}</body></html>"


def _write_page(site, path: str, html: str) -> None:
    (site / path).mkdir(parents=True, exist_ok=True)
    (site / path / "index.html").write_text(html)


@pytest.fixture
def site(tmp_path):
    _write_page(tmp_path, "blog", INDEX.replace("</body>", _pushes(POST) + "</body>"))
    return tmp_path


def test_the_posts_index_keys_a_post_by_its_path_with_a_slash(site):
    assert list(blog_search.posts_index(site)) == ["/blog/a-post/"]


def test_the_posts_index_keeps_the_date_and_categories(site):
    post = blog_search.posts_index(site)["/blog/a-post/"]
    assert (post["date"], post["categories"]) == ("2026-09-23", ["Tech"])


def test_the_posts_index_names_each_author_with_a_local_image(site):
    author = blog_search.posts_index(site)["/blog/a-post/"]["authors"][0]
    assert author == {
        "name": "Ada Lovelace",
        "image": "/sanity/images/sy1jschh/production/" + "a" * 40 + "-800x800.jpg",
    }


def test_the_search_page_drops_the_next_js_scripts():
    page = blog_search.search_page(INDEX)
    assert "chunks/a.js" not in page and "__next_f" not in page


def test_the_search_page_keeps_the_runtime_config():
    assert '<script src="/js/runtime-config.js"></script>' in blog_search.search_page(
        INDEX
    )


def test_the_search_page_loads_the_search_script():
    assert blog_search.SEARCH_SCRIPT in blog_search.search_page(INDEX)


def test_write_puts_the_search_page_under_the_blog(site):
    blog_search.write(site)
    assert (site / "blog" / "search" / "index.html").is_file()


def test_write_reports_how_many_posts_it_knows(site):
    assert blog_search.write(site) == 1


def test_an_id_that_is_not_an_image_has_no_url():
    assert blog_search.image_url("file-abc-pdf") == ""


def test_the_posts_index_reads_the_numbered_pages_too(site):
    second = dict(POST, pathname="/blog/another-post")
    _write_page(site, "blog/page/2", _listing_page(second))
    assert "/blog/another-post/" in blog_search.posts_index(site)


def test_payload_posts_skip_objects_that_are_not_posts():
    author = {"_createdAt": "2020-01-01T00:00:00Z", "firstName": "Ada"}
    assert blog_search.payload_posts(_listing_page(author)) == []


def test_payload_posts_read_a_post_split_across_pushes():
    assert blog_search.payload_posts(_listing_page(POST)) == [POST]
