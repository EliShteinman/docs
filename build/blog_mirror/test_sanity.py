"""Tests for the dataset query. No network: these cover how the query is built.

The formatting test exists because the query is a str.format template and GROQ
projections are braces. An unescaped `{firstName,lastName,role}` was read as a
format field and raised KeyError at the first fetch -- after the package had
already passed every other test.
"""

import pytest

from build.blog_mirror.sanity import (
    API_HOST,
    DOCUMENT_TYPE,
    _QUERY,
    query_url,
)


def _rendered() -> str:
    return _QUERY.format(doc_type=DOCUMENT_TYPE, start=0, end=40)


def test_the_query_template_formats_without_a_missing_field():
    assert _rendered()


def test_the_query_selects_blog_posts():
    assert '_type=="blogPost"' in _rendered()


def test_the_query_pages_by_id_so_paging_cannot_skip_a_post():
    """Ordering by date would let two posts sharing a date swap between pages."""
    assert "order(_id)" in _rendered()


def test_the_author_projection_survives_formatting():
    """Its braces are GROQ, not format fields."""
    assert "author[]->{firstName,lastName,role}" in _rendered()


def test_categories_are_dereferenced_to_their_titles():
    assert "categories[]->title" in _rendered()


def test_the_url_is_built_against_the_cdn_host():
    assert query_url("*").startswith(API_HOST)


@pytest.mark.parametrize("character", ["{", "}", '"', " "])
def test_query_characters_are_encoded_into_the_url(character):
    assert character not in query_url(f'*[a=="{character}"]').split("?", 1)[1]
