"""Tests for reading redis.io's page-builder pages."""

from build.site_mirror.pages import (
    DROPPED_SECTIONS,
    KNOWN_SECTIONS,
    render_page,
    section_types,
    strip_html,
)


def _resolve(reference, _alt=""):
    return f"/images/site-mirror/{reference}.webp"


def _block(text, style="normal"):
    return {
        "_type": "block",
        "style": style,
        "children": [{"_type": "span", "text": text, "marks": []}],
        "markDefs": [],
    }


def test_a_title_arrives_as_an_html_fragment():
    assert strip_html("<h2>Benefits</h2>") == "Benefits"


def test_a_title_can_also_arrive_as_portable_text():
    """Some /solutions/ sections carry Portable Text where a string is expected."""
    assert strip_html([_block("Fraud detection")]) == "Fraud detection"


def test_metadata_keys_do_not_leak_into_a_title():
    assert "block" not in strip_html([_block("Session management")])


def test_a_title_of_an_unexpected_type_becomes_empty_rather_than_raising():
    """The section loses its heading; the run does not lose the page."""
    assert strip_html(42) == "" and strip_html(None) == ""


def test_html_entities_are_decoded():
    assert strip_html("<h2>Redis &amp; Valkey</h2>") == "Redis & Valkey"


def test_a_rich_text_section_renders_its_content():
    page = {"sections": [{"_type": "richTextSection", "content": [_block("Body text.")]}]}
    assert render_page(page, _resolve) == "Body text."


def test_a_section_title_becomes_a_heading():
    page = {"sections": [{"_type": "twoColDefaultSection", "title": "<h2>Benefits</h2>"}]}
    assert render_page(page, _resolve) == "## Benefits"


def test_the_hero_section_does_not_repeat_the_page_title_as_a_heading():
    page = {"sections": [{"_type": "headerSimpleSection", "title": "Cluster", "content": [_block("Intro.")]}]}
    assert render_page(page, _resolve) == "Intro."


def test_card_entries_become_sub_headings_with_their_text():
    page = {
        "sections": [
            {
                "_type": "cardGridSection",
                "title": "<h2>Benefits</h2>",
                "cards": [{"title": "Fast", "content": [_block("Sub-millisecond.")]}],
            }
        ]
    }
    assert render_page(page, _resolve) == "## Benefits\n\n### Fast\n\nSub-millisecond."


def test_accordion_items_are_read_from_their_description():
    page = {
        "sections": [
            {
                "_type": "accordionSection",
                "title": "<h2>FAQs</h2>",
                "accordionItems": [{"title": "Why?", "description": [_block("Because.")]}],
            }
        ]
    }
    assert "### Why?\n\nBecause." in render_page(page, _resolve)


def test_a_video_section_becomes_a_link():
    page = {"sections": [{"_type": "twoColDefaultSection", "videoUrl": "https://youtu.be/x"}]}
    assert render_page(page, _resolve) == "[Watch the video](https://youtu.be/x)"


def test_marketing_sections_are_dropped():
    page = {
        "sections": [
            {"_type": "richTextSection", "content": [_block("Real.")]},
            {"_type": "closingCtaSection", "title": "<h2>Want to learn more?</h2>"},
            {"_type": "cardCarouselSection", "title": "<h2>Related resources</h2>"},
        ]
    }
    assert render_page(page, _resolve) == "Real."


def test_an_unknown_section_contributes_nothing():
    page = {"sections": [{"_type": "richTextSection", "content": [_block("Kept.")]}, {"_type": "brandNew"}]}
    assert render_page(page, _resolve) == "Kept."


def test_section_types_are_reported_so_a_new_layout_is_noticed():
    page = {"sections": [{"_type": "brandNew"}]}
    assert section_types(page) - KNOWN_SECTIONS == {"brandNew"}


def test_the_dropped_sections_count_as_known():
    assert DROPPED_SECTIONS <= KNOWN_SECTIONS
