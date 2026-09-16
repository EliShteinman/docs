"""Tests for the endpoint itself: the contract, and what it does when Redis is not there."""

import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from resp import RespError
from search import main


class FakeConnection:
    """Records what was sent, and answers from a scripted list."""

    def __init__(self, replies: list | None = None) -> None:
        self.sent: list[list[str]] = []
        self.closed = False
        self._replies = list(replies or [])

    def send_command(self, args: list[str]) -> None:
        self.sent.append(args)

    def read_reply(self) -> object:
        return self._replies.pop(0) if self._replies else [0]

    def close(self) -> None:
        self.closed = True


@pytest.fixture
def client():
    return main.app.test_client()


def _use(monkeypatch, connection):
    monkeypatch.setattr(main.CONNECTIONS, "get", lambda: connection)
    monkeypatch.setattr(main.CONNECTIONS, "discard", lambda: None)
    return connection


def test_a_hit_is_returned_in_the_shape_the_modal_reads(monkeypatch, client):
    _use(
        monkeypatch,
        FakeConnection(
            [
                [
                    1,
                    "doc:/develop/ai",
                    # WITHSCORES puts the score between the key and the fields.
                    "4.5",
                    [
                        "title",
                        "<b>Vector</b> search",
                        "body",
                        "about <b>vector</b>",
                        "url",
                        "/develop/ai",
                        "hierarchy",
                        json.dumps(["Welcome to Redis Docs", "Develop with Redis"]),
                        "source",
                        "docs",
                        "version",
                        "latest",
                        "product",
                        "",
                    ],
                ]
            ]
        ),
    )
    body = client.get("/search?q=vector*&p=all").get_json()
    assert body == {
        "total": 1,
        "results": [
            {
                "title": "<b>Vector</b> search",
                "section_title": "",
                "hierarchy": ["Welcome to Redis Docs", "Develop with Redis"],
                "body": "about <b>vector</b>",
                "url": "/develop/ai",
                "source": "docs",
                "version": "latest",
                "product": "",
                "score": 4.5,
            }
        ],
    }


def test_a_row_links_to_the_best_ranked_copy_of_the_page(monkeypatch, client):
    """The modal keeps the last result per title; only the first is sent."""
    crumbs = json.dumps(["Welcome to Redis Docs", "Operate"])
    _use(
        monkeypatch,
        FakeConnection(
            [
                [
                    2,
                    "doc:/operate/rs/rack",
                    [
                        "title",
                        "Rack-zone awareness",
                        "url",
                        "/operate/rs/rack/",
                        "hierarchy",
                        crumbs,
                    ],
                    "doc:/operate/rs/7.4/rack",
                    [
                        "title",
                        "Rack-zone awareness",
                        "url",
                        "/operate/rs/7.4/rack/",
                        "hierarchy",
                        crumbs,
                    ],
                ]
            ]
        ),
    )
    body = client.get("/search?q=rack*&p=all").get_json()
    assert [result["url"] for result in body["results"]] == ["/operate/rs/rack/"]


def test_no_matches_answers_the_empty_body_with_a_200(monkeypatch, client):
    _use(monkeypatch, FakeConnection([[0]]))
    response = client.get("/search?q=zzzz*&p=all")
    assert response.status_code == 200
    assert response.get_json() == {"total": 0, "results": []}


def test_an_empty_query_never_reaches_redis(monkeypatch, client):
    connection = _use(monkeypatch, FakeConnection())
    client.get("/search?q=&p=all")
    assert connection.sent == []


def test_the_product_filter_reaches_the_query(monkeypatch, client):
    connection = _use(monkeypatch, FakeConnection([[0]]))
    client.get("/search?q=vector*&p=rs")
    assert "@product:{rs}" in connection.sent[0][2]


def test_the_site_parameter_is_accepted_and_ignored(monkeypatch, client):
    """The live service returns identical results with and without it."""
    connection = _use(monkeypatch, FakeConnection([[0]]))
    client.get("/search?q=vector*&p=all&site=%2Fdocs%2Flatest%2F")
    assert not any("docs" in str(argument) for argument in connection.sent[0][3:])


def test_a_rejected_query_answers_no_results_rather_than_an_error(monkeypatch, client):
    _use(monkeypatch, FakeConnection([RespError("Syntax error")]))
    response = client.get("/search?q=vector*&p=all")
    assert response.status_code == 200
    assert response.get_json()["total"] == 0


def test_a_dead_connection_is_not_reported_as_an_empty_corpus(monkeypatch, client):
    """503, not an empty 200: "nothing matched" and "nothing answered" differ."""
    class Broken(FakeConnection):
        def read_reply(self) -> object:
            raise OSError("connection reset")

    _use(monkeypatch, Broken())
    response = client.get("/search?q=vector*&p=all")
    assert response.status_code == 503
    assert response.get_json() == {"total": 0, "results": [], "error": "search unavailable"}


def test_a_rejected_query_says_so_in_the_body(monkeypatch, client):
    """The modal renders "No results" from a 200, so the reason goes in the body."""
    _use(monkeypatch, FakeConnection([RespError("Syntax error")]))
    assert client.get("/search?q=vector*&p=all").get_json()["error"] == "query rejected"


def test_an_answer_of_nothing_carries_no_error(monkeypatch, client):
    _use(monkeypatch, FakeConnection([[0]]))
    assert "error" not in client.get("/search?q=zzzz*&p=all").get_json()


def _limit_and_offset(sent: list[str]) -> list[str]:
    at = sent.index("LIMIT")
    return sent[at + 1 : at + 3]


def test_the_modal_sending_neither_gets_the_page_size_it_always_had(monkeypatch, client):
    connection = _use(monkeypatch, FakeConnection([[0]]))
    client.get("/search?q=vector*&p=all")
    assert _limit_and_offset(connection.sent[0]) == ["0", str(main.config.RESULT_LIMIT)]


def test_a_caller_can_page_past_the_first_results(monkeypatch, client):
    connection = _use(monkeypatch, FakeConnection([[0]]))
    client.get("/search?q=vector*&p=all&limit=5&offset=10")
    assert _limit_and_offset(connection.sent[0]) == ["10", "5"]


@pytest.mark.parametrize(
    "query_string,expected",
    [
        ("limit=99999", ["0", str(main.config.MAX_RESULT_LIMIT)]),
        ("limit=0", ["0", "1"]),
        ("limit=banana", ["0", str(main.config.RESULT_LIMIT)]),
        ("offset=-5", ["0", str(main.config.RESULT_LIMIT)]),
        ("offset=99999", [str(main.config.MAX_OFFSET), str(main.config.RESULT_LIMIT)]),
    ],
    ids=["over cap", "under one", "not a number", "negative", "past the cap"],
)
def test_paging_arguments_are_clamped_rather_than_refused(monkeypatch, client, query_string, expected):
    connection = _use(monkeypatch, FakeConnection([[0]]))
    client.get(f"/search?q=vector*&p=all&{query_string}")
    assert _limit_and_offset(connection.sent[0]) == expected


def test_readiness_fails_until_the_index_exists(monkeypatch, client):
    _use(monkeypatch, FakeConnection([RespError("Unknown index name")]))
    assert client.get("/healthz").status_code == 503


def test_readiness_passes_once_the_index_is_there(monkeypatch, client):
    _use(monkeypatch, FakeConnection([["index_name", "docs"]]))
    assert client.get("/healthz").status_code == 200
