"""Tests for the query the modal's parameters turn into, and the reply it gets back.

The expectations here were measured against the live redis.io service, not
inferred from the partial.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from search.query import build_query, one_per_row, parse_reply, search_command, to_results


def _result(title: str, url: str, first_crumb: str = "Welcome to Redis Docs") -> dict:
    return {"title": title, "url": url, "hierarchy": [first_crumb, "Operate"]}


def test_the_last_token_keeps_the_prefix_marker_the_modal_sent():
    assert build_query("vector search*", "all") == "vector search*"


def test_earlier_tokens_are_matched_exactly():
    """`vect search*` answers 0 on the live service: "vect" is not a prefix there."""
    assert build_query("vect search*", "all").startswith("vect ")


def test_words_are_anded_by_leaving_them_space_separated():
    assert build_query("vector search", "all") == "vector search"


def test_query_syntax_in_the_typed_text_never_reaches_the_parser():
    assert build_query("a|b", "all") == "a b"


def test_a_dotted_command_is_split_the_way_the_index_split_it():
    """`JSON\\.SET*` answered 0 on a real index; `JSON SET*` finds the page."""
    assert build_query("JSON.SET*", "all") == "JSON SET*"


def test_a_hyphen_is_not_left_for_the_parser_to_read_as_exclusion():
    """`Active-Active*` answered 0 on a real index: the hyphen negates."""
    assert build_query("Active-Active*", "all") == "Active Active*"


def test_an_underscore_stays_inside_the_term_like_it_does_in_the_index():
    assert build_query("eviction_policy*", "all") == "eviction_policy*"


def test_punctuation_after_the_last_term_keeps_the_prefix_marker():
    assert build_query("redis-*", "all") == "redis*"


def test_a_word_of_only_punctuation_is_dropped():
    assert build_query("vector -- search*", "all") == "vector search*"


def test_the_prefix_marker_is_not_escaped_into_a_literal():
    assert build_query("vec*", "all").endswith("*")


def test_an_empty_query_produces_nothing_to_search_for():
    assert build_query("   ", "all") == ""


def test_a_specific_product_adds_a_tag_filter():
    assert build_query("vector*", "rs") == "vector* @product:{rs}"


def test_all_products_adds_no_filter():
    assert "@product" not in build_query("vector*", "all")


def test_a_missing_product_parameter_adds_no_filter():
    assert "@product" not in build_query("vector*", "")


def test_a_hyphenated_product_is_escaped_for_the_tag_parser():
    assert "redis\\-data\\-integration" in build_query("x*", "redis-data-integration")


def test_an_unknown_product_is_passed_through_to_match_nothing():
    """The live service answers p=banana with total 0, not an error."""
    assert "@product:{banana}" in build_query("x*", "banana")


def test_the_result_cap_matches_the_live_service():
    command = search_command("docs", "x*", 30)
    assert command[command.index("LIMIT") : command.index("LIMIT") + 3] == ["LIMIT", "0", "30"]


def test_highlighting_uses_the_same_tags_the_live_service_returns():
    command = search_command("docs", "x*", 30)
    assert "<b>" in command and "</b>" in command


def test_parse_reply_reads_the_total_from_the_first_element():
    total, _ = parse_reply([312, "doc:/a", ["title", "A"]])
    assert total == 312


def test_parse_reply_pairs_the_returned_fields():
    _, documents = parse_reply([1, "doc:/a", ["title", "A", "url", "/a"]])
    assert documents == [{"title": "A", "url": "/a"}]


def test_parse_reply_of_an_empty_index_is_empty():
    assert parse_reply([0]) == (0, [])


def test_parse_reply_survives_an_unexpected_shape():
    assert parse_reply("not a list") == (0, [])


def test_a_result_carries_the_five_fields_the_modal_reads():
    results = to_results([{"title": "A", "url": "/a", "body": "b", "hierarchy": '["Root","A"]'}])
    assert set(results[0]) == {"title", "section_title", "hierarchy", "body", "url"}


def test_section_title_is_always_empty_like_the_live_service():
    assert to_results([{"title": "A"}])[0]["section_title"] == ""


def test_hierarchy_is_decoded_back_into_a_list():
    stored = json.dumps(["Welcome to Redis Docs", "Develop with Redis"])
    assert to_results([{"hierarchy": stored}])[0]["hierarchy"] == [
        "Welcome to Redis Docs",
        "Develop with Redis",
    ]


def test_an_unreadable_hierarchy_becomes_an_empty_trail():
    assert to_results([{"hierarchy": "{["}])[0]["hierarchy"] == []


def test_a_versioned_copy_below_its_current_page_is_dropped():
    results = [
        _result("Rack-zone awareness", "/operate/rs/rack"),
        _result("Rack-zone awareness", "/operate/rs/7.4/rack"),
    ]
    assert [result["url"] for result in one_per_row(results)] == ["/operate/rs/rack"]


def test_the_same_title_under_another_heading_is_a_row_of_its_own():
    results = [_result("Overview", "/operate/rs"), _result("Overview", "/blog/overview", "Blog")]
    assert len(one_per_row(results)) == 2


def test_a_result_without_a_trail_is_kept():
    assert one_per_row([{"title": "A", "url": "/a", "hierarchy": []}]) == [
        {"title": "A", "url": "/a", "hierarchy": []}
    ]


def test_the_scorer_is_named_rather_than_left_to_the_redis_default():
    """Redis 8 defaults to BM25STD, which ranks this corpus badly -- see query.py."""
    command = search_command("docs", "vector*", 30)
    assert command[command.index("SCORER") + 1] == "BM25"
