"""Tests for the request path: parsing a typed line, and what it refuses.

The rewriting these commands go through is covered in test_namespace.py and the
isolation it buys in test_isolation.py. What is left here is the layer between
the HTTP body and the wire.
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(__file__))

import main
from resp import RespError
from sessions import Session


class FakeConnection:
    """Records what was sent, and answers from a scripted list."""

    def __init__(self, replies: list | None = None) -> None:
        self.closed = False
        self.sent: list[list[str]] = []
        self._replies = list(replies or [])

    def send_command(self, args: list[str]) -> None:
        self.sent.append(args)

    def read_reply(self) -> object:
        return self._replies.pop(0) if self._replies else "OK"

    def close(self) -> None:
        self.closed = True


@pytest.fixture(autouse=True)
def unnamespaced(monkeypatch):
    """These tests are about the request path, so leave the keys alone."""
    monkeypatch.setattr(main.config, "NAMESPACE_ENABLED", False)


@pytest.fixture
def connection() -> FakeConnection:
    return FakeConnection()


@pytest.fixture
def session(connection) -> Session:
    return Session(sid="s", connection=connection)


# --- parsing ---------------------------------------------------------------


def test_a_command_is_split_into_arguments(session, connection):
    main.run_command(session, "SET greeting hello")

    assert connection.sent == [["SET", "greeting", "hello"]]


def test_a_quoted_argument_stays_one_argument(session, connection):
    main.run_command(session, 'SET greeting "hello there"')

    assert connection.sent == [["SET", "greeting", "hello there"]]


def test_an_unbalanced_quote_is_reported_not_raised(session):
    assert main.run_command(session, 'SET k "unclosed')["error"]


def test_an_unbalanced_quote_never_reaches_redis(session, connection):
    main.run_command(session, 'SET k "unclosed')

    assert connection.sent == []


def test_an_empty_line_is_reported(session):
    assert main.run_command(session, "   ")["error"]


# --- reply shapes the widget depends on ------------------------------------


def test_a_simple_string_is_tagged_as_a_status(session):
    """The widget prints OK unquoted and a bulk string quoted."""
    from resp import RespStatus

    session.connection = FakeConnection([RespStatus("OK")])

    assert main.run_command(session, "SET k v")["status"]


def test_an_error_is_flagged(session):
    session.connection = FakeConnection([RespError("ERR no such key")])

    assert main.run_command(session, "GET k")["error"]


def test_a_bulk_string_is_not_a_status(session):
    session.connection = FakeConnection(["hello"])

    assert "status" not in main.run_command(session, "GET k")


# --- commands the ACL cannot deny ------------------------------------------


def test_reset_is_refused_by_the_proxy(session):
    assert main.run_command(session, "RESET")["error"]


def test_reset_never_reaches_redis(session, connection):
    main.run_command(session, "reset")

    assert connection.sent == []


def test_the_refusal_reads_like_redis(session):
    assert "no permissions" in main.run_command(session, "RESET")["value"]


def test_reset_is_what_the_proxy_denies():
    assert main.PROXY_DENIED == frozenset({"RESET"})


# --- keeping the namespace out of sight ------------------------------------


def test_the_prefix_is_taken_out_of_error_text():
    """Redis quotes the key it was given, which carries the session prefix."""
    from namespace import Namespace

    message = main._readable("WRONGTYPE against key 'abc:product:1'", Namespace("abc"))

    assert message == "WRONGTYPE against key 'product:1'"


def test_error_text_is_untouched_when_namespacing_is_off():
    assert main._readable("ERR whatever", None) == "ERR whatever"


def test_a_command_is_refused_when_the_key_lookup_is_down(session, connection, monkeypatch):
    """Running it as typed would write outside the reader's namespace."""
    from namespace import KeyLookupUnavailable

    monkeypatch.setattr(main.config, "NAMESPACE_ENABLED", True)
    monkeypatch.setattr(
        main._rewriter, "rewrite",
        lambda argv, ns: (_ for _ in ()).throw(KeyLookupUnavailable("down")),
    )

    assert main.run_command(session, "SET k v")["error"]


def test_a_refused_command_never_reaches_redis(session, connection, monkeypatch):
    from namespace import KeyLookupUnavailable

    monkeypatch.setattr(main.config, "NAMESPACE_ENABLED", True)
    monkeypatch.setattr(
        main._rewriter, "rewrite",
        lambda argv, ns: (_ for _ in ()).throw(KeyLookupUnavailable("down")),
    )
    main.run_command(session, "SET k v")

    assert connection.sent == []
