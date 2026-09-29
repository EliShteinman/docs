import json

import pytest

from build.marketing_mirror import blog_search, feeds

POST = {
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


@pytest.fixture
def site(tmp_path):
    feeds.batch_file(tmp_path, "blog", 0).parent.mkdir(parents=True)
    feeds.batch_file(tmp_path, "blog", 0).write_text(json.dumps({"posts": [POST]}))
    (tmp_path / "blog").mkdir()
    (tmp_path / "blog" / "index.html").write_text(INDEX)
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
