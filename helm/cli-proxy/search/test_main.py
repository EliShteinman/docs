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
                    [
                        "title",
                        "<b>Vector</b> search",
                        "body",
                        "about <b>vector</b>",
                        "url",
                        "/develop/ai",
                        "hierarchy",
                        json.dumps(["Welcome to Redis Docs", "Develop with Redis"]),
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


def test_a_dead_connection_answers_no_results_rather_than_a_500(monkeypatch, client):
    class Broken(FakeConnection):
        def read_reply(self) -> object:
            raise OSError("connection reset")

    _use(monkeypatch, Broken())
    response = client.get("/search?q=vector*&p=all")
    assert response.status_code == 200
    assert response.get_json() == {"total": 0, "results": []}


def test_readiness_fails_until_the_index_exists(monkeypatch, client):
    _use(monkeypatch, FakeConnection([RespError("Unknown index name")]))
    assert client.get("/healthz").status_code == 503


def test_readiness_passes_once_the_index_is_there(monkeypatch, client):
    _use(monkeypatch, FakeConnection([["index_name", "docs"]]))
    assert client.get("/healthz").status_code == 200
