"""Tests for the dataset query. No network: these cover how the query is built.

The formatting test exists because the query is a str.format template and GROQ
projections are braces. An unescaped `{firstName,lastName,role}` was read as a
format field and raised KeyError at the first fetch -- after the package had
already passed every other test.
"""

import pytest

from build.site_mirror.sanity import (
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


def test_every_query_filters_the_source_to_english():
    """A translated document publishes at the English document's URL.

    The blog was the one query without this clause, and the source holds
    exactly one translated blog document: a German test post,
    "[Dev] Test Blog for DE". It was mirrored, published at
    /blog/dev-test-blog-for-de/ and indexed for search.
    """
    from build.site_mirror import sanity

    assert 'language == "en"' in sanity._QUERY
    assert 'language == "en"' in sanity._PAGE_QUERY


def test_no_mirrored_blog_post_is_a_translation_or_a_test_document():
    """The corpus on disk must not carry what the filter excludes."""
    from pathlib import Path

    root = Path(__file__).resolve().parents[2] / "content" / "blog"
    offenders = [
        f.name for f in root.glob("*.md")
        if "[Dev]" in f.read_text(encoding="utf-8", errors="replace")[:400]
    ]
    assert not offenders, f"dev/test posts published to readers: {offenders}"
