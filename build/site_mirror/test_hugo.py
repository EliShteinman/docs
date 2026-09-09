"""Tests for the frontmatter and file layout of a mirrored post."""

from pathlib import Path

from build.site_mirror.hugo import (
    author_names,
    byline,
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
    post = {"title": "X", "authors": [{"firstName": "Tony", "lastName": "Wu"}]}
    assert '- "Tony Wu"' in front_matter(post)


def test_a_post_with_no_description_omits_the_key_rather_than_emptying_it():
    assert "description:" not in front_matter({"title": "X"}, "")


def test_the_description_comes_from_the_first_real_paragraph():
    """Not from the source's tagline, which says "News & Media" on 1,060 posts."""
    body = "![tile](/images/site-mirror/x.webp)\n\n## Heading\n\nThe actual opening sentence."
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


AUTHOR = {"firstName": "Tony", "lastName": "Wu", "role": "Sr. Solution Architect"}


def test_an_author_name_is_built_from_the_two_fields_that_exist():
    """The author document has no `name`; asking for one yields no bylines at all."""
    assert author_names({"authors": [AUTHOR]}) == ["Tony Wu"]


def test_an_author_with_only_a_first_name_still_counts():
    assert author_names({"authors": [{"firstName": "Antirez"}]}) == ["Antirez"]


def test_a_post_with_no_authors_yields_no_names():
    assert author_names({}) == []


def test_the_byline_carries_who_wrote_it_and_when():
    line = byline({"authors": [AUTHOR], "publishDate": "2020-06-29T10:00:00Z"})
    assert "By Tony Wu" in line and "Published 29 June 2020" in line


def test_the_role_is_shown_for_a_single_author():
    assert "Sr. Solution Architect" in byline({"authors": [AUTHOR]})


def test_an_update_later_than_publication_is_shown():
    line = byline({"publishDate": "2020-06-29T00:00:00Z", "_updatedAt": "2025-03-27T00:00:00Z"})
    assert "updated 27 March 2025" in line


def test_an_update_on_the_publication_day_is_not_repeated():
    line = byline({"publishDate": "2020-06-29T00:00:00Z", "_updatedAt": "2020-06-29T23:00:00Z"})
    assert "updated" not in line


def test_a_post_with_no_credits_at_all_gets_no_byline():
    assert byline({}) == ""


def test_a_malformed_date_does_not_reach_the_byline():
    assert byline({"publishDate": "not-a-date"}) == ""


def test_the_byline_is_written_into_the_body_so_it_travels_with_the_content():
    out = render_post({"title": "T", "authors": [AUTHOR]}, "Body.")
    assert "By Tony Wu" in out.split("---", 2)[2]


def test_the_source_update_time_becomes_hugos_lastmod():
    assert "lastmod: 2025-03-27" in front_matter({"title": "X", "_updatedAt": "2025-03-27T22:15:06Z"})


def test_a_body_that_opens_by_repeating_the_title_loses_the_heading():
    """The glossary writes its term as an H1; every theme renders one already."""
    from build.site_mirror.hugo import drop_repeated_title

    assert drop_repeated_title("# ACID\n\nText.", "ACID") == "Text."


def test_a_different_opening_heading_is_kept():
    from build.site_mirror.hugo import drop_repeated_title

    body = "# Something else\n\nText."
    assert drop_repeated_title(body, "ACID") == body


def test_a_visible_document_carries_no_hidden_flag():
    assert "hidden" not in front_matter({"title": "X"}, hidden=False)


def test_a_nested_path_publishes_its_hyphenated_alias():
    """redis.io answers both forms; only one of them is a real path."""
    from build.site_mirror.hugo import flattened_alias

    assert flattened_alias("tutorials", "develop/dotnet/streams/stream-basics") == (
        "/tutorials/develop-dotnet-streams-stream-basics/"
    )


def test_a_flat_path_needs_no_alias():
    from build.site_mirror.hugo import flattened_alias

    assert flattened_alias("compare", "valkey") == ""


def test_aliases_reach_the_frontmatter():
    matter = front_matter({"title": "X"}, aliases=("/tutorials/a-b/",))
    assert "aliases:" in matter and '- "/tutorials/a-b/"' in matter
