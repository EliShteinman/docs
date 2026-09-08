"""Tests for rebuilding the breadcrumb trail the modal renders."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from search.hierarchy import BreadcrumbIndex
from search.sources import Document

ROOT = "Welcome to Redis Docs"


def _document(url: str, title: str) -> Document:
    return Document(
        doc_id=url, title=title, url=url, body="", version="", product="", source="docs"
    )


def _redisvl_index() -> BreadcrumbIndex:
    """The ancestors of the page this was checked against on the live service."""
    return BreadcrumbIndex.from_documents(
        ROOT,
        [
            _document("/develop", "Develop with Redis"),
            _document("/develop/ai", "Redis for AI and search"),
            _document("/develop/ai/redisvl", "RedisVL"),
            _document("/develop/ai/redisvl/concepts", "Concepts"),
            _document("/develop/ai/redisvl/concepts/utilities", "Utilities"),
        ],
    )


def test_trail_matches_the_live_service():
    crumbs = _redisvl_index().crumbs_for("/develop/ai/redisvl/concepts/utilities")
    assert crumbs == [
        ROOT,
        "Develop with Redis",
        "Redis for AI and search",
        "RedisVL",
        "Concepts",
        "Utilities",
    ]


def test_trail_starts_at_the_root_so_the_modal_groups_correctly():
    crumbs = _redisvl_index().crumbs_for("/develop/ai/redisvl")
    assert crumbs[0] == ROOT


def test_the_modal_reads_the_row_labels_from_positions_one_and_two():
    crumbs = _redisvl_index().crumbs_for("/develop/ai/redisvl/concepts/utilities")
    assert (crumbs[1], crumbs[2]) == ("Develop with Redis", "Redis for AI and search")


def test_a_missing_ancestor_is_skipped_not_filled():
    index = BreadcrumbIndex.from_documents(
        ROOT,
        [
            _document("/develop", "Develop with Redis"),
            _document("/develop/ai/redisvl", "RedisVL"),
        ],
    )
    assert index.crumbs_for("/develop/ai/redisvl") == [ROOT, "Develop with Redis", "RedisVL"]


def test_a_page_with_no_ancestors_is_just_the_root_and_itself():
    index = BreadcrumbIndex.from_documents(ROOT, [_document("/commands", "Commands")])
    assert index.crumbs_for("/commands") == [ROOT, "Commands"]


def test_a_trailing_slash_resolves_to_the_same_trail():
    index = _redisvl_index()
    assert index.crumbs_for("/develop/ai/") == index.crumbs_for("/develop/ai")
