"""Tests for pointing redis.io links at the pages this image already serves."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from build.doc_links import (
    LEGACY,
    alias_targets,
    apply_to_tree,
    legacy_urls,
    local_path,
    published_paths,
    rewrite_legacy,
)

MIRRORED = """---
title: "A post"
---

Read [the old docs](https://redis.io/docs/interact/search/) and
[start free](https://redis.io/try-free/) today.
"""

UPSTREAM = """---
title: A documentation page
---

See [the old docs](https://redis.io/docs/interact/search/) and
[downloads](https://redis.io/downloads/).
"""


def test_a_legacy_documentation_url_is_recognised():
    assert LEGACY.search("https://redis.io/docs/interact/search/")
    assert LEGACY.search("http://redis.io/topics/pubsub")


def test_the_current_documentation_url_is_left_to_the_build_rule_that_handles_it():
    """`/docs/latest/` is rewritten by sed in both pipelines; this must not touch it."""
    assert not LEGACY.search("https://redis.io/docs/latest/develop/")


def test_the_legacy_domains_are_recognised_too():
    assert LEGACY.search("https://www.redis.com/docs/getting-started/")


def test_a_mapped_link_is_pointed_at_the_local_page():
    text, count = rewrite_legacy(
        "see [docs](https://redis.io/docs/interact/search/)",
        {"https://redis.io/docs/interact/search/": "/develop/search/"},
    )
    assert "(/develop/search/)" in text and count == 1


def test_an_unmapped_link_is_left_exactly_as_it_was():
    """Nothing is guessed: a URL nobody observed stays what the author wrote."""
    original = "see [docs](https://redis.io/docs/never-seen/)"
    text, count = rewrite_legacy(original, {})
    assert text == original and count == 0


def test_a_fragment_survives_the_rewrite():
    text, _ = rewrite_legacy(
        "[x](https://redis.io/docs/interact/search/#scoring)",
        {"https://redis.io/docs/interact/search/": "/develop/search/"},
    )
    assert text == "[x](/develop/search/#scoring)"


def test_a_landing_outside_the_documentation_maps_to_nothing():
    assert local_path("https://redis.io/try-free/") == ""


def test_a_documentation_landing_becomes_the_path_this_image_serves():
    assert (
        local_path("https://redis.io/docs/latest/develop/clients/")
        == "/develop/clients/"
    )


def _tree(tmp_path: Path) -> Path:
    content = tmp_path / "content"
    (content / "blog").mkdir(parents=True)
    (content / "blog" / "post.md").write_text(MIRRORED, encoding="utf-8")
    (content / "page.md").write_text(UPSTREAM, encoding="utf-8")
    return content


def test_every_page_gets_its_legacy_links_pointed_inward(tmp_path):
    content = _tree(tmp_path)
    apply_to_tree(
        content, {"https://redis.io/docs/interact/search/": "/develop/search/"}
    )
    assert "(/develop/search/)" in (content / "blog" / "post.md").read_text()
    assert "(/develop/search/)" in (content / "page.md").read_text()


def test_the_counts_report_what_was_done(tmp_path):
    content = _tree(tmp_path)
    touched, fixed = apply_to_tree(
        content, {"https://redis.io/docs/interact/search/": "/develop/search/"}
    )
    assert (touched, fixed) == (2, 2)


def test_collecting_urls_ignores_the_fragment_so_one_page_is_one_entry(tmp_path):
    content = tmp_path / "content"
    content.mkdir()
    (content / "a.md").write_text(
        "[x](https://redis.io/docs/interact/search/#one) [y](https://redis.io/docs/interact/search/#two)",
        encoding="utf-8",
    )
    assert legacy_urls(content) == ["https://redis.io/docs/interact/search/"]


def test_a_page_publishes_at_its_path(tmp_path):
    content = tmp_path / "content"
    (content / "develop").mkdir(parents=True)
    (content / "develop" / "clients.md").write_text(
        "---\ntitle: X\n---\n", encoding="utf-8"
    )
    assert "/develop/clients/" in published_paths(content)


def test_a_section_index_publishes_at_its_directory(tmp_path):
    content = tmp_path / "content"
    (content / "develop").mkdir(parents=True)
    (content / "develop" / "_index.md").write_text(
        "---\ntitle: X\n---\n", encoding="utf-8"
    )
    assert "/develop/" in published_paths(content)


def test_an_alias_counts_as_published(tmp_path):
    """937 documentation pages carry one, and they are how a moved page still answers."""
    content = tmp_path / "content"
    content.mkdir()
    (content / "a.md").write_text(
        "---\naliases:\n- /old/path\ntitle: X\n---\n", encoding="utf-8"
    )
    assert "/old/path/" in published_paths(content)


def test_a_declared_url_counts_as_published(tmp_path):
    content = tmp_path / "content"
    content.mkdir()
    (content / "a.md").write_text(
        '---\nurl: "/blog/a-post/"\ntitle: X\n---\n', encoding="utf-8"
    )
    assert "/blog/a-post/" in published_paths(content)


def test_a_leaf_bundle_publishes_at_its_directory(tmp_path):
    content = tmp_path / "content"
    (content / "develop" / "eviction").mkdir(parents=True)
    (content / "develop" / "eviction" / "index.md").write_text(
        "---\ntitle: X\n---\n", encoding="utf-8"
    )
    assert "/develop/eviction/" in published_paths(content)


def test_an_alias_maps_to_the_page_that_declares_it(tmp_path):
    content = tmp_path / "content"
    (content / "develop").mkdir(parents=True)
    (content / "develop" / "pubsub.md").write_text(
        "---\ntitle: X\naliases:\n- /develop/interact/pubsub\n---\n", encoding="utf-8"
    )
    assert alias_targets(content) == {"/develop/interact/pubsub/": "/develop/pubsub/"}
