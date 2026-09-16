"""Tests for pointing redis.io links at the pages this image already serves."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from build.site_mirror.doc_links import (
    LEGACY,
    apply_to_tree,
    is_mirrored,
    legacy_urls,
    local_path,
    published_paths,
    rewrite_legacy,
    unlink_unservable,
)

MIRRORED = """---
title: "A post"
mirrored: true
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
    assert local_path("https://redis.io/docs/latest/develop/clients/") == "/develop/clients/"


def test_a_dead_link_becomes_the_words_it_was_written_as():
    text, removed = unlink_unservable("[start free](https://redis.io/try-free/) today")
    assert text == "start free today" and removed == 1


def test_an_image_is_never_unlinked():
    """An image with no source is not an improvement on a broken one."""
    original = "![a chart](https://redis.io/images/x.png)"
    assert unlink_unservable(original) == (original, 0)


def test_a_link_to_somewhere_else_entirely_is_left_alone():
    original = "[the client](https://github.com/redis/redis-py)"
    assert unlink_unservable(original) == (original, 0)


def test_a_link_that_already_points_inward_is_left_alone():
    original = "[the docs](/develop/clients/)"
    assert unlink_unservable(original) == (original, 0)


def test_a_mirrored_page_is_told_apart_from_an_upstream_one():
    assert is_mirrored(MIRRORED)
    assert not is_mirrored(UPSTREAM)


def test_a_marker_in_the_body_does_not_make_a_page_mirrored():
    assert not is_mirrored('---\ntitle: X\n---\n\nThe frontmatter says `mirrored: true`.\n')


def _tree(tmp_path: Path) -> Path:
    content = tmp_path / "content"
    (content / "blog").mkdir(parents=True)
    (content / "blog" / "post.md").write_text(MIRRORED, encoding="utf-8")
    (content / "page.md").write_text(UPSTREAM, encoding="utf-8")
    return content


def test_both_kinds_of_page_get_their_legacy_links_pointed_inward(tmp_path):
    content = _tree(tmp_path)
    apply_to_tree(content, {"https://redis.io/docs/interact/search/": "/develop/search/"})
    assert "(/develop/search/)" in (content / "blog" / "post.md").read_text()
    assert "(/develop/search/)" in (content / "page.md").read_text()


def test_only_the_mirror_has_its_dead_links_unlinked(tmp_path):
    """Upstream's prose is upstream's: this fork rewrites its links, not its sentences."""
    content = _tree(tmp_path)
    apply_to_tree(content, {})
    assert "start free today" in (content / "blog" / "post.md").read_text()
    assert "[downloads](https://redis.io/downloads/)" in (content / "page.md").read_text()


def test_the_counts_report_what_was_done(tmp_path):
    content = _tree(tmp_path)
    touched, legacy, removed = apply_to_tree(
        content, {"https://redis.io/docs/interact/search/": "/develop/search/"}
    )
    assert (touched, legacy, removed) == (2, 2, 1)


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
    (content / "develop" / "clients.md").write_text("---\ntitle: X\n---\n", encoding="utf-8")
    assert "/develop/clients/" in published_paths(content)


def test_a_section_index_publishes_at_its_directory(tmp_path):
    content = tmp_path / "content"
    (content / "develop").mkdir(parents=True)
    (content / "develop" / "_index.md").write_text("---\ntitle: X\n---\n", encoding="utf-8")
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
    """The mirror writes one on every page it produces."""
    content = tmp_path / "content"
    content.mkdir()
    (content / "a.md").write_text(
        '---\nurl: "/blog/a-post/"\ntitle: X\n---\n', encoding="utf-8"
    )
    assert "/blog/a-post/" in published_paths(content)


def test_a_link_another_rule_makes_local_is_never_unlinked():
    """Ordering must not decide whether a link to a page in this image survives."""
    for url in (
        "https://redis.io/docs/latest/develop/clients/",
        "https://redis.io/commands/set/",
        "https://redis.io/blog/a-post/",
        "https://redis.io/tutorials/",
    ):
        original = f"[x]({url})"
        assert unlink_unservable(original) == (original, 0), url


def test_a_legacy_link_nobody_could_resolve_is_unlinked_like_any_other(tmp_path):
    """54 of the 145 lead nowhere even on redis.io; inside the mirror they are dead."""
    content = tmp_path / "content"
    (content / "blog").mkdir(parents=True)
    (content / "blog" / "post.md").write_text(
        "---\ntitle: X\nmirrored: true\n---\n\n[gone](https://redis.io/docs/never-seen/)\n",
        encoding="utf-8",
    )
    apply_to_tree(content, {})
    assert (content / "blog" / "post.md").read_text().endswith("gone\n")
