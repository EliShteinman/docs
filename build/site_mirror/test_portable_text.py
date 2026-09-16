"""Tests for rendering Portable Text as markdown.

The expectations come from the shapes actually present in the corpus: fourteen
block types across all 1,108 posts, checked before this was written.
"""

from build.site_mirror.portable_text import render


def _resolve(reference, _alt=""):
    return f"/images/blog/{reference}.webp"


def _block(text, style="normal", marks=None, defs=None, **extra):
    return {
        "_type": "block",
        "style": style,
        "children": [{"_type": "span", "text": text, "marks": marks or []}],
        "markDefs": defs or [],
        **extra,
    }


def test_a_paragraph_renders_as_itself():
    assert render([_block("Hello")], _resolve) == "Hello"


def test_a_heading_becomes_the_matching_markdown_level():
    assert render([_block("Title", style="h2")], _resolve) == "## Title"


def test_a_bolded_heading_is_not_bolded_twice():
    """Most of the corpus bolds its own headings; the level already carries it."""
    assert render([_block("Title", style="h2", marks=["strong"])], _resolve) == "## Title"


def test_emphasis_still_applies_inside_a_paragraph():
    assert render([_block("hi", marks=["strong"])], _resolve) == "**hi**"


def test_inline_code_is_marked_up():
    assert render([_block("GET", marks=["inlineCode"])], _resolve) == "`GET`"


def test_a_link_with_an_href_is_rendered():
    defs = [{"_key": "k", "_type": "link", "href": "https://example.com"}]
    out = render([_block("here", marks=["k"], defs=defs)], _resolve)
    assert out == "[here](https://example.com)"


def test_a_link_in_sanitys_other_shape_is_also_rendered():
    defs = [{"_key": "k", "_type": "link", "linkType": "external", "externalLink": "https://x.test"}]
    assert render([_block("here", marks=["k"], defs=defs)], _resolve) == "[here](https://x.test)"


def test_a_blog_link_is_pointed_at_the_mirror():
    defs = [{"_key": "k", "_type": "link", "href": "https://redis.io/blog/x/"}]
    assert render([_block("post", marks=["k"], defs=defs)], _resolve) == "[post](/blog/x/)"


def test_a_link_that_points_nowhere_stays_as_plain_text():
    defs = [{"_key": "k", "_type": "link", "linkType": "internal", "anchor": {}}]
    assert render([_block("text", marks=["k"], defs=defs)], _resolve) == "text"


def test_bullet_items_stay_together_without_blank_lines_between_them():
    blocks = [_block("one", listItem="bullet", level=1), _block("two", listItem="bullet", level=1)]
    assert render(blocks, _resolve) == "- one\n- two"


def test_a_numbered_list_uses_numeric_markers():
    assert render([_block("one", listItem="number", level=1)], _resolve) == "1. one"


def test_a_nested_item_is_indented_by_its_level():
    assert render([_block("deep", listItem="bullet", level=2)], _resolve) == "  - deep"


def test_a_code_block_carries_its_language():
    block = {"_type": "blockContentBlogCode", "codeSnippet": {"code": "x = 1", "language": "python"}}
    assert render([block], _resolve) == "```python\nx = 1\n```"


def test_sanitys_own_language_names_are_translated():
    """`plain` means no highlighting and `jscript` means JavaScript."""
    block = {"_type": "blockContentBlogCode", "codeSnippet": {"code": "x", "language": "plain"}}
    assert render([block], _resolve).startswith("```\n")


def test_an_empty_code_block_is_dropped():
    block = {"_type": "blockContentBlogCode", "codeSnippet": {"code": "   "}}
    assert render([block], _resolve) == ""


def test_a_table_renders_with_a_header_separator():
    block = {
        "_type": "blockContentBlogTable",
        "table": {"rows": [{"cells": ["A", "B"]}, {"cells": ["1", "2"]}]},
    }
    assert render([block], _resolve) == "| A | B |\n|---|---|\n| 1 | 2 |"


def test_a_ragged_table_is_padded_so_the_columns_line_up():
    block = {
        "_type": "blockContentBlogTable",
        "table": {"rows": [{"cells": ["A", "B"]}, {"cells": ["1"]}]},
    }
    assert render([block], _resolve).endswith("| 1 |  |")


def test_a_pipe_inside_a_cell_does_not_split_the_column():
    block = {"_type": "blockContentBlogTable", "table": {"rows": [{"cells": ["a|b"]}]}}
    assert "a\\|b" in render([block], _resolve)


def test_an_image_becomes_a_reference_to_the_mirrored_file():
    block = {
        "_type": "blockContentBlogImage",
        "image": {"altText": "a chart", "asset": {"_ref": "image-abc-1x1-png"}},
    }
    assert render([block], _resolve) == "![a chart](/images/blog/image-abc-1x1-png.webp)"


def test_an_image_that_could_not_be_fetched_is_left_out():
    block = {"_type": "blockContentBlogImage", "image": {"asset": {"_ref": "x"}}}
    assert render([block], lambda *_: "") == ""


def test_a_video_becomes_a_link_because_the_player_is_off_site():
    block = {"_type": "blockContentBlogVideo", "videoUrl": "https://youtu.be/x", "buttonLabel": "Watch"}
    assert render([block], _resolve) == "[Watch](https://youtu.be/x)"


def test_a_quote_is_rendered_as_a_blockquote():
    block = {"_type": "blockContentBlogQuote", "quote": [_block("quoted")]}
    assert render([block], _resolve) == "> quoted"


def test_an_iframe_is_named_rather_than_carried():
    """It points at hosts that do not resolve offline; a dead frame looks like a fault."""
    block = {"_type": "blockContentBlogEmbed", "embed": "<iframe src='https://x'></iframe>"}
    assert render([block], _resolve) == "*(interactive chart, not available offline)*"


def test_an_anchor_point_becomes_a_heading_with_an_explicit_id():
    block = {"_type": "blockContentAnchorPoint", "identifier": {"current": "langcache"}, "title": "LangCache"}
    assert render([block], _resolve) == "### LangCache {#langcache}"


def test_a_divider_becomes_a_rule():
    assert render([{"_type": "divider"}], _resolve) == "---"


def test_marketing_interrupters_are_dropped():
    """They point at pages an air-gapped reader cannot reach."""
    blocks = [_block("real"), {"_type": "blockContentCtaInterrupter", "title": "Try Redis Cloud"}]
    assert render(blocks, _resolve) == "real"


def test_button_rows_are_dropped_too():
    blocks = [{"_type": "blockContentBlogButtons", "buttons": [{"label": "Claim credit"}]}]
    assert render(blocks, _resolve) == ""


def test_an_unknown_block_type_is_skipped_rather_than_breaking_the_post():
    assert render([_block("kept"), {"_type": "somethingNew"}], _resolve) == "kept"


def test_paragraphs_are_separated_by_a_blank_line():
    assert render([_block("one"), _block("two")], _resolve) == "one\n\ntwo"
