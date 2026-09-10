"""Tests for building the index: the commands sent, and what is stored per document."""

import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from resp import RespError
from search.hierarchy import BreadcrumbIndex
from search.indexer import (
    IndexingError,
    allow_single_character_prefixes,
    create_index,
    index_documents,
)
from search.sources import Document


class FakeConnection:
    def __init__(self, replies: list | None = None) -> None:
        self.sent: list[list[str]] = []
        self._replies = list(replies or [])

    def send_command(self, args: list[str]) -> None:
        self.sent.append(args)

    def read_reply(self) -> object:
        return self._replies.pop(0) if self._replies else "OK"

    def close(self) -> None:
        pass


def _document(url: str = "/operate/rs/x", title: str = "X") -> Document:
    return Document(
        doc_id=url, title=title, url=url + "/", body="body text", version="7.4",
        product="rs", source="docs",
    )


def _crumbs() -> BreadcrumbIndex:
    return BreadcrumbIndex("Welcome to Redis Docs", {"/operate/rs/x": "X"})


def test_one_character_prefixes_are_enabled_to_match_the_live_service():
    """The modal fires on the first keystroke, and redis.io answers `v*` with hits."""
    connection = FakeConnection()
    allow_single_character_prefixes(connection)
    assert connection.sent == [["FT.CONFIG", "SET", "MINPREFIX", "1"]]


def test_a_previous_index_is_dropped_with_its_documents():
    connection = FakeConnection()
    create_index(connection, "docs", "doc:")
    assert connection.sent[0] == ["FT.DROPINDEX", "docs", "DD"]


@pytest.mark.parametrize(
    "wording",
    [
        # Redis 8 wording, seen against redis:8.10.0-alpine.
        "SEARCH_INDEX_NOT_FOUND Index not found: docs",
        # Older wording, kept because the chart does not pin the reader's Redis.
        "Unknown index name",
    ],
)
def test_a_first_run_tolerates_there_being_no_index_to_drop(wording):
    connection = FakeConnection([RespError(wording), "OK"])
    create_index(connection, "docs", "doc:")
    assert connection.sent[1][0] == "FT.CREATE"


def test_an_unexpected_drop_failure_stops_the_build():
    connection = FakeConnection([RespError("READONLY")])
    with pytest.raises(IndexingError):
        create_index(connection, "docs", "doc:")


def test_the_schema_weights_the_title_above_the_body():
    connection = FakeConnection()
    create_index(connection, "docs", "doc:")
    schema = connection.sent[1]
    assert schema[schema.index("title") + 2 : schema.index("title") + 4] == ["WEIGHT", "5"]


def test_the_source_tag_is_in_the_schema_from_the_first_day():
    """So adding the blog later does not mean reindexing for a schema change."""
    connection = FakeConnection()
    create_index(connection, "docs", "doc:")
    assert "source" in connection.sent[1]


def test_each_document_is_written_under_the_key_prefix():
    connection = FakeConnection()
    index_documents(connection, [_document()], _crumbs(), "doc:", 500)
    assert connection.sent[0][1] == "doc:/operate/rs/x"


def test_the_stored_hierarchy_is_the_trail_the_response_returns():
    connection = FakeConnection()
    index_documents(connection, [_document()], _crumbs(), "doc:", 500)
    fields = dict(zip(connection.sent[0][2::2], connection.sent[0][3::2]))
    assert json.loads(fields["hierarchy"]) == ["Welcome to Redis Docs", "X"]


def test_the_crumbs_are_indexed_as_searchable_text():
    connection = FakeConnection()
    index_documents(connection, [_document()], _crumbs(), "doc:", 500)
    fields = dict(zip(connection.sent[0][2::2], connection.sent[0][3::2]))
    assert fields["crumbs"] == "Welcome to Redis Docs X"


def test_a_write_failure_stops_the_build():
    connection = FakeConnection([RespError("OOM")])
    with pytest.raises(IndexingError):
        index_documents(connection, [_document()], _crumbs(), "doc:", 500)


def test_documents_are_written_in_batches():
    connection = FakeConnection()
    documents = [_document(f"/operate/rs/{n}") for n in range(5)]
    assert index_documents(connection, documents, _crumbs(), "doc:", 2) == 5


def test_a_current_page_keeps_its_full_relevance():
    from search.indexer import document_score

    assert document_score("latest") == "1"


def test_an_older_version_keeps_only_part_of_it():
    """45% of a real index is versioned copies, and without this they crowd out
    the current page -- "rack zone awareness" answered with 7.22 first."""
    from search.indexer import document_score

    assert float(document_score("7.4")) < 1


def test_an_untagged_page_is_treated_as_current():
    from search.indexer import document_score

    assert document_score("") == "1"


def test_the_index_multiplies_relevance_by_that_score():
    connection = FakeConnection()
    create_index(connection, "docs", "doc:")
    create = connection.sent[1]
    assert create[create.index("SCORE_FIELD") + 1] == "docscore"


def test_every_document_carries_its_score():
    connection = FakeConnection()
    index_documents(connection, [_document()], _crumbs(), "doc:", 500)
    fields = dict(zip(connection.sent[0][2::2], connection.sent[0][3::2]))
    assert fields["docscore"] == "0.3"
