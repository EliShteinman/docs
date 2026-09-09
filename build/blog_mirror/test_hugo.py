"""Tests for the frontmatter and file layout of a mirrored post."""

from pathlib import Path

from build.blog_mirror.hugo import (
    permalink,
    file_name,
    front_matter,
    prune_removed,
    render_post,
    summarize,
    write_post,
    write_section_index,
)


def test_a_slug_becomes_a_flat_markdown_file_name():
    assert file_name("/redisgraph-eol/", "fallback") == "redisgraph-eol.md"


def test_a_post_without_a_usable_slug_falls_back_to_its_id():
    assert file_name("", "abc123") == "abc123.md"


def test_characters_a_file_system_would_object_to_are_replaced():
    assert file_name("/a b/c?d/", "x") == "a-b-c-d.md"


def test_every_post_is_hidden_from_the_docs_sidebar():
    """1,100 posts in the sidebar would bury the documentation it exists to navigate."""
    assert "hidden: true" in front_matter({"title": "X"})


def test_a_title_with_a_colon_survives_the_frontmatter():
    matter = front_matter({"title": "Agent interoperability: a complete explainer"})
    assert '"Agent interoperability: a complete explainer"' in matter


def test_the_publish_date_is_reduced_to_a_day():
    assert "date: 2023-07-05" in front_matter({"title": "X", "publishDate": "2023-07-05T05:00:49.000Z"})


def test_source_categories_do_not_land_in_the_docs_taxonomy():
    """`categories` is one of Hugo's default taxonomies and the docs already use it."""
    matter = front_matter({"title": "X", "categories": ["Tech DE"]})
    assert "blogCategories:" in matter
    assert "\ncategories:" not in matter


def test_authors_are_carried_when_the_source_names_them():
    assert "- \"Redis\"" in front_matter({"title": "X", "authors": ["Redis"]})


def test_a_post_with_no_description_omits_the_key_rather_than_emptying_it():
    assert "description:" not in front_matter({"title": "X"}, "")


def test_the_description_comes_from_the_first_real_paragraph():
    """Not from the source's tagline, which says "News & Media" on 1,060 posts."""
    body = "![tile](/images/blog/x.webp)\n\n## Heading\n\nThe actual opening sentence."
    assert summarize(body) == "The actual opening sentence."


def test_the_description_is_stripped_of_markdown():
    assert summarize("A [link](http://x) and **bold**.") == "A link and bold."


def test_a_long_opening_paragraph_is_shortened():
    assert len(summarize("word " * 200)) <= 203


def test_a_post_with_nothing_quotable_gets_no_description():
    assert summarize("## Only a heading") == ""


def test_a_rendered_post_puts_the_body_after_the_frontmatter():
    out = render_post({"title": "X"}, "Body text.")
    assert out.startswith("---\n") and out.rstrip().endswith("Body text.")


def test_writing_a_post_creates_the_section_directory(tmp_path: Path):
    path = write_post(tmp_path / "blog", "a.md", "---\n---\n")
    assert path.exists()


def test_the_section_index_is_written_so_no_post_is_unlinked(tmp_path: Path):
    assert write_section_index(tmp_path).name == "_index.md"


def test_a_post_removed_upstream_is_removed_here(tmp_path: Path):
    write_post(tmp_path, "gone.md", "x")
    write_post(tmp_path, "kept.md", "x")
    assert prune_removed(tmp_path, {"kept.md"}) == 1
    assert not (tmp_path / "gone.md").exists()


def test_pruning_never_deletes_the_section_index(tmp_path: Path):
    write_section_index(tmp_path)
    prune_removed(tmp_path, set())
    assert (tmp_path / "_index.md").exists()


def test_a_post_publishes_at_the_slug_the_source_uses():
    """config.toml carries a dated permalink rule for a section named `blog`."""
    assert permalink("/redisgraph-eol/") == "/blog/redisgraph-eol/"


def test_the_permalink_is_written_into_the_frontmatter():
    assert 'url: "/blog/x/"' in front_matter({"title": "T", "slug": "/x/"})


def test_a_post_with_no_slug_falls_back_to_the_section_root():
    assert permalink("") == "/blog/"
