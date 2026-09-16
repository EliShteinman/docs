"""Tests for building the index: the commands sent, and what is stored per document."""

import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from resp import RespError
from search.hierarchy import BreadcrumbIndex
from search import config
from search.indexer import (
    IndexingError,
    VersionLadder,
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


def _versioned(tree: str, version: str) -> Document:
    return Document(
        doc_id=f"{tree}/{version}/page", title="Page", url=f"{tree}/{version}/page/",
        body="body text", version=version, product="rs", source="docs",
    )


def _ladder(*documents: Document) -> VersionLadder:
    return VersionLadder.from_documents(list(documents))


def _score(ladder: VersionLadder, document: Document) -> float:
    return float(ladder.score_for(document))


def test_a_current_page_keeps_its_full_relevance():
    current = Document(
        doc_id="/operate/rs/page", title="Page", url="/operate/rs/page/", body="b",
        version="latest", product="rs", source="docs",
    )
    assert _ladder(current).score_for(current) == "1"


def test_an_archived_version_keeps_only_part_of_it():
    """45% of a real index is versioned copies, and without this they crowd out
    the current page -- "rack zone awareness" answered with 7.22 first."""
    archived = _versioned("/operate/rs", "7.4")
    assert _score(_ladder(archived), archived) < 1


def test_an_untagged_page_is_treated_as_current():
    untagged = Document(
        doc_id="/blog/post", title="Post", url="/blog/post/", body="b",
        version="", product="", source="blog",
    )
    assert _ladder(untagged).score_for(untagged) == "1"


def test_a_newer_archived_version_outranks_an_older_one():
    """The archive has an order of its own: 8.0 is a better answer than 7.4."""
    old, middle, new = (_versioned("/operate/rs", v) for v in ("7.4", "7.8", "8.0"))
    ladder = _ladder(old, middle, new)
    assert _score(ladder, old) < _score(ladder, middle) < _score(ladder, new)


def test_the_newest_archive_still_loses_to_the_current_documentation():
    """Redis Software's numbered trees stop at 8.0; 8.2 publishes as `latest`."""
    newest = _versioned("/operate/rs", "8.0")
    assert _score(_ladder(newest), newest) < 1


def test_a_two_part_version_is_ordered_by_number_not_by_text():
    """7.22 comes after 7.4 -- as text it sorts before it."""
    later, earlier = _versioned("/operate/rs", "7.22"), _versioned("/operate/rs", "7.4")
    ladder = _ladder(later, earlier)
    assert _score(ladder, later) > _score(ladder, earlier)


def test_each_product_is_ranked_inside_its_own_tree():
    """RedisVL 0.3 and Redis Software 8.0 are both the newest of their archive."""
    redisvl = _versioned("/develop/ai/redisvl", "0.3")
    software = _versioned("/operate/rs", "8.0")
    ladder = _ladder(redisvl, software, _versioned("/operate/rs", "7.4"))
    assert _score(ladder, redisvl) == _score(ladder, software)


def test_the_oldest_version_keeps_the_floor():
    oldest = _versioned("/operate/rs", "7.22")
    ladder = _ladder(oldest, _versioned("/operate/rs", "8.0"))
    assert _score(ladder, oldest) == config.VERSION_WEIGHT


def test_a_version_the_page_path_does_not_carry_keeps_the_floor():
    """Nothing to rank it against, so it is not promoted over a real tree."""
    stray = Document(
        doc_id="/operate/rs/page", title="Page", url="/operate/rs/page/", body="b",
        version="7.4", product="rs", source="docs",
    )
    assert _score(_ladder(stray), stray) == config.VERSION_WEIGHT


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


def _mirrored(url: str, title: str, source: str) -> Document:
    return Document(
        doc_id=url, title=title, url=url + "/", body="body text", version="",
        product="", source=source,
    )


def test_a_mirrored_section_heads_its_own_group_instead_of_the_docs_root():
    """hierarchy[0] is the heading the modal files a result under.

    A customer story or a product comparison listed beneath "Welcome to Redis
    Docs" reads to a reader as documentation, which it is not.
    """
    section = _mirrored("/customers", "Customer stories", "site")
    story = _mirrored("/customers/acme", "Acme", "site")
    crumbs = BreadcrumbIndex.from_documents("Welcome to Redis Docs", [section, story])
    connection = FakeConnection()
    index_documents(connection, [story], crumbs, "doc:", 500)
    fields = dict(zip(connection.sent[0][2::2], connection.sent[0][3::2]))
    assert json.loads(fields["hierarchy"]) == ["Customer stories", "Acme"]


def test_a_documentation_page_still_sits_under_the_docs_root():
    connection = FakeConnection()
    index_documents(connection, [_document()], _crumbs(), "doc:", 500)
    fields = dict(zip(connection.sent[0][2::2], connection.sent[0][3::2]))
    assert json.loads(fields["hierarchy"])[0] == "Welcome to Redis Docs"
