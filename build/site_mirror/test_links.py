"""Tests for pointing the blog's cross-references at the mirrored copy."""

import pytest

from build.site_mirror.links import localize


@pytest.mark.parametrize(
    "url",
    [
        "https://redis.io/blog/redisgraph-eol/",
        "https://redis.com/blog/redisgraph-eol/",
        "https://redislabs.com/blog/redisgraph-eol/",
        "http://www.redislabs.com/blog/redisgraph-eol/",
        "https://redis.io/en/blog/redisgraph-eol/",
    ],
)
def test_every_spelling_of_the_blog_resolves_locally(url):
    """99 of the 184 blog links in the docs use the legacy domains."""
    assert localize(url) == "/blog/redisgraph-eol/"


def test_a_link_without_a_trailing_slash_gets_one():
    """Hugo publishes a post as a directory; without the slash nginx redirects."""
    assert localize("https://redis.com/blog/x") == "/blog/x/"


def test_the_blog_root_becomes_the_section_index():
    assert localize("https://redis.io/blog/") == "/blog/"


def test_a_fragment_is_preserved_and_no_slash_is_inserted_before_it():
    assert localize("https://redis.io/blog/a#section") == "/blog/a#section"


def test_a_documentation_link_is_left_alone():
    """Only blog-to-blog links are guaranteed to resolve in the mirror."""
    url = "https://redis.io/docs/latest/develop/"
    assert localize(url) == url


def test_an_unrelated_link_is_left_alone():
    assert localize("https://github.com/redis/redis") == "https://github.com/redis/redis"


def test_a_domain_that_merely_starts_the_same_is_not_matched():
    url = "https://redis.io.evil.example/blog/x"
    assert localize(url) == url


def test_an_empty_url_survives():
    assert localize("") == ""


def test_an_author_page_link_becomes_plain_text():
    """Author and tag listings are navigation over the blog, not writing, so
    they are not mirrored and a link to one would dead-end."""
    assert localize("https://redis.io/blog/author/guy-royse/") == ""


def test_a_tag_listing_link_becomes_plain_text():
    assert localize("https://redis.io/blog/tag/redis/") == ""


def test_a_real_post_is_still_localized():
    assert localize("https://redis.io/blog/real-post/") == "/blog/real-post/"


def test_a_root_relative_author_link_is_also_stripped():
    """The source writes some of its own links relative, with no host to match on."""
    assert localize("/blog/author/dave/") == ""


def test_a_root_relative_post_link_is_left_alone():
    assert localize("/blog/real-post/") == "/blog/real-post/"


def test_a_relative_link_outside_the_blog_is_untouched():
    assert localize("/operate/rs/") == "/operate/rs/"
