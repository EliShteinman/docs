import pytest

from build.marketing_mirror import moved_pages
from build.marketing_mirror.fetcher import Moved
from build.marketing_mirror.pages import html_file

OLD = "/blog/old-post/"


@pytest.fixture
def written(tmp_path):
    moved_pages.write(tmp_path, {OLD: "/blog/new-post"}, {"/blog/new-post/"})
    return html_file(tmp_path, OLD).read_text()


def test_a_page_moved_within_the_mirror_refreshes_to_its_new_path(written):
    assert '<meta http-equiv="refresh" content="0; url=/blog/new-post/">' in written


def test_the_moved_page_has_no_main_for_the_search_feed(written):
    assert "<main" not in written


def test_a_page_moved_out_of_the_mirror_gets_no_page(tmp_path):
    moved_pages.write(tmp_path, {OLD: "/feature-form/"}, {"/blog/"})
    assert not html_file(tmp_path, OLD).exists()


def test_write_reports_how_many_pages_it_wrote(tmp_path):
    moved = {OLD: "/blog/", "/solutions/x/": "/feature-form/"}
    assert moved_pages.write(tmp_path, moved, {"/blog/"}) == 1


def test_the_target_is_escaped_in_the_page():
    assert "url=/blog/&quot;x/" in moved_pages.redirect_page('/blog/"x/')


def test_moved_carries_its_target():
    assert Moved("https://redis.io/a/", "/b/").target == "/b/"
