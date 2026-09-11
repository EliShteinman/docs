"""Tests for reading the docs feed into indexable documents."""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from search.sources import clean_body, load_documents, read_feed, to_document


def test_link_targets_are_dropped_and_link_text_is_kept():
    """The placeholder in a link target must never become a search term."""
    body = clean_body("Install [Redis Cloud](__DOCS_BASE_URL__/operate/rc) today")
    assert "__DOCS_BASE_URL__" not in body
    assert "Redis Cloud" in body


def test_image_syntax_is_reduced_to_its_alt_text():
    assert clean_body("![a diagram](/images/x.png)") == "a diagram"


def test_markdown_emphasis_does_not_survive_into_the_index():
    assert clean_body("**bold** and `code`") == "bold and code"


def test_underscore_emphasis_does_not_survive_into_the_index():
    assert clean_body("_italic_ and __bold__") == "italic and bold"


def test_an_underscore_inside_a_name_is_kept_so_the_name_stays_one_term():
    assert clean_body("Set `eviction_policy` to noeviction") == "Set eviction_policy to noeviction"


def test_whitespace_is_collapsed():
    assert clean_body("one\n\n   two") == "one two"


def test_a_record_becomes_a_document_with_a_relative_url():
    document = to_document({"url": "https://redis.io/operate/rs/x", "title": "X", "summary": "c"})
    assert document.url == "/operate/rs/x"


def test_a_document_carries_the_product_derived_from_its_url():
    document = to_document({"url": "/operate/rs/x", "title": "X", "summary": "c"})
    assert document.product == "rs"


def test_a_document_carries_the_version_the_fork_tagged_it_with():
    document = to_document({"url": "/operate/rs/7.4/x", "title": "X", "summary": "", "version": "7.4"})
    assert document.version == "7.4"


def test_a_feed_without_the_version_step_leaves_the_tag_empty():
    document = to_document({"url": "/operate/rs/x", "title": "X", "summary": ""})
    assert document.version == ""


def _record_with_sections(*sections: dict) -> dict:
    return {"url": "/x", "title": "X", "summary": "A summary.", "sections": list(sections)}


def test_the_summary_alone_is_indexed_when_a_record_has_no_sections():
    document = to_document({"url": "/x", "title": "X", "summary": "a summary"})
    assert document.body == "a summary"


def test_the_text_of_every_section_is_indexed():
    """The feed's real shape: prose lives in sections, and there is no content field."""
    record = _record_with_sections({"title": "Set up", "text": "Set eviction_policy first."})
    assert "eviction_policy" in to_document(record).body


def test_a_section_heading_is_indexed_with_its_text():
    record = _record_with_sections({"title": "Rack awareness", "text": "Spread the shards."})
    assert "Rack awareness" in to_document(record).body


def test_the_summary_is_kept_alongside_the_sections():
    record = _record_with_sections({"title": "Set up", "text": "Body."})
    assert to_document(record).body.startswith("A summary.")


def test_the_code_block_placeholder_is_not_indexed():
    record = _record_with_sections({"title": "Run it", "text": "Type this:\n\n[code example]"})
    assert "example" not in to_document(record).body


def test_a_record_without_a_title_is_not_indexable():
    assert to_document({"url": "/x", "summary": "c"}) is None


def test_a_record_without_a_url_is_not_indexable():
    assert to_document({"title": "X", "summary": "c"}) is None


def test_a_malformed_line_does_not_cost_the_whole_feed(tmp_path):
    feed = tmp_path / "docs.ndjson"
    feed.write_text(
        json.dumps({"url": "/a", "title": "A", "summary": ""})
        + "\n{ not json\n"
        + json.dumps({"url": "/b", "title": "B", "summary": ""})
        + "\n",
        encoding="utf-8",
    )
    assert len(list(read_feed(feed))) == 2


def test_blank_lines_are_ignored(tmp_path):
    feed = tmp_path / "docs.ndjson"
    feed.write_text(json.dumps({"url": "/a", "title": "A"}) + "\n\n\n", encoding="utf-8")
    assert len(load_documents(feed)) == 1


def test_a_second_source_is_tagged_so_it_can_be_told_apart(tmp_path):
    """What adding the blog will rely on: same reader, different source tag."""
    feed = tmp_path / "blog.ndjson"
    feed.write_text(json.dumps({"url": "/blog/x", "title": "X"}) + "\n", encoding="utf-8")
    assert load_documents(feed, source="blog")[0].source == "blog"


def test_the_link_keeps_the_trailing_slash_and_the_key_does_not():
    document = to_document({"url": "https://redis.io/operate/rs/", "title": "X"})
    assert (document.url, document.doc_id) == ("/operate/rs/", "/operate/rs")


def test_a_mirrored_blog_post_is_tagged_as_blog():
    """Blog posts share the feed with the docs; where they live tells them apart."""
    document = to_document({"url": "/blog/redisgraph-eol/", "title": "X"})
    assert document.source == "blog"


def test_a_documentation_page_is_tagged_as_docs():
    assert to_document({"url": "/operate/rs/x", "title": "X"}).source == "docs"


def test_a_blog_post_carries_no_product_so_it_is_not_hidden_by_the_filter():
    assert to_document({"url": "/blog/x/", "title": "X"}).product == ""


def test_every_mirrored_section_is_told_apart_from_the_documentation():
    """A mirrored page must not be tagged docs: that tag decides its heading."""
    for url in (
        "/tutorials/how-to-build-a-rate-limiter/",
        "/technology/redis-enterprise-cluster-architecture/",
        "/compare/redis-vs-mongodb/",
        "/solutions/fraud-detection/",
        "/customers/some-company/",
        "/resources/architecture-diagrams/caching/",
    ):
        assert to_document({"url": url, "title": "X"}).source == "site", url


def test_a_mirrored_sections_own_index_is_told_apart_too():
    """to_path drops the trailing slash, so the index arrives without one."""
    assert to_document({"url": "/technology/", "title": "Technology"}).source == "site"
    assert to_document({"url": "/blog/", "title": "Blog"}).source == "blog"


def test_a_mirrored_glossary_term_stays_with_the_documentation():
    """Its terms publish inside the documentation's own /glossary/ section.

    Their heading should be the documentation's, not a heading of their own --
    unlike every other mirrored section, which lives at a path of its own.
    """
    document = to_document({"url": "/glossary/acid-transactions/", "title": "ACID"})
    assert document.source == "docs"


def test_a_path_that_merely_starts_with_a_mirrored_name_is_not_mirrored():
    """/comparefoo is not /compare, and /blogging-guide is not /blog."""
    assert to_document({"url": "/comparefoo/x", "title": "X"}).source == "docs"
    assert to_document({"url": "/blogging-guide", "title": "X"}).source == "docs"
