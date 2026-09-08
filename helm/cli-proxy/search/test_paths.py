"""Tests for normalising a feed record's url into a comparable path."""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from search.paths import ancestors, segments, to_path


@pytest.mark.parametrize(
    "url,expected",
    [
        ("/develop/ai", "/develop/ai"),
        ("/develop/ai/", "/develop/ai"),
        ("develop/ai", "/develop/ai"),
        ("/", "/"),
        ("", "/"),
    ],
)
def test_to_path_normalises_relative_urls(url, expected):
    assert to_path(url) == expected


def test_to_path_strips_scheme_and_host():
    assert to_path("https://redis.io/develop/ai/") == "/develop/ai"


def test_to_path_keeps_a_path_prefix_the_build_added():
    assert to_path("https://redis.io/docs/latest/develop/") == "/docs/latest/develop"


def test_to_path_drops_the_fragment():
    assert to_path("/develop/ai#embeddings") == "/develop/ai"


def test_to_path_drops_the_query_string():
    assert to_path("/develop/ai?tab=python") == "/develop/ai"


def test_to_path_of_a_bare_host_is_the_root():
    assert to_path("https://redis.io") == "/"


def test_segments_are_outermost_first():
    assert segments("/develop/ai/redisvl") == ["develop", "ai", "redisvl"]


def test_ancestors_walk_every_prefix_including_the_page():
    assert ancestors("/develop/ai/redisvl") == ["/develop", "/develop/ai", "/develop/ai/redisvl"]


def test_ancestors_of_the_root_are_empty():
    assert ancestors("/") == []


def test_to_href_keeps_the_trailing_slash_hugo_publishes():
    """Without it every result click costs an nginx 301 to add the slash back."""
    from search.paths import to_href

    assert to_href("https://redis.io/develop/ai/") == "/develop/ai/"


def test_to_href_leaves_a_slashless_url_alone():
    from search.paths import to_href

    assert to_href("/commands/get") == "/commands/get"


def test_to_href_of_the_root_is_a_single_slash():
    from search.paths import to_href

    assert to_href("https://redis.io/") == "/"
