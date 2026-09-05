"""Tests for the rewriting that gives each session its own slice of the keyspace.

Unit tests below drive CommandRewriter and ReplyFilter with a stubbed key
resolver, so they pin the rewriting rules without needing Redis. The end-to-end
half lives in test_isolation.py, which runs two sessions against a real server
and checks they cannot see each other.
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(__file__))

from namespace import CommandRewriter, KeyResolver, Namespace, ReplyFilter
from resp import RespError, RespStatus

SID = "abc123"
PREFIX = "abc123:"


@pytest.fixture
def ns() -> Namespace:
    return Namespace(SID)


@pytest.fixture
def rewriter():
    """A rewriter whose key lookup answers from a table instead of Redis."""
    table = {
        "GET": [1], "SET": [1], "DEL": [1, 2], "TYPE": [1], "EXPIRE": [1],
        "HSET": [1], "ZADD": [1], "XADD": [1], "HSCAN": [1], "SSCAN": [1],
        "ZSCAN": [1], "JSON.SET": [1], "TS.CREATE": [1], "BF.ADD": [1],
        "RENAME": [1, 2], "MSET": [1, 3],
    }

    class StubResolver(KeyResolver):
        def __init__(self) -> None:
            super().__init__(lambda argv: RespError("unused"))

        def keys_of(self, argv):
            positions = table.get(argv[0].upper(), [])
            return [argv[i] for i in positions if i < len(argv)]

    return CommandRewriter(StubResolver(), scan_min_count=10000)


# --- the namespace itself --------------------------------------------------


def test_apply_adds_the_prefix(ns):
    assert ns.apply("product:1") == PREFIX + "product:1"


def test_apply_is_idempotent(ns):
    """A value that made a round trip must not come back double-prefixed."""
    assert ns.apply(ns.apply("product:1")) == PREFIX + "product:1"


def test_strip_removes_the_prefix(ns):
    assert ns.strip(PREFIX + "product:1") == "product:1"


def test_strip_leaves_a_foreign_name_alone(ns):
    assert ns.strip("other:product:1") == "other:product:1"


def test_owns_is_true_for_our_keys(ns):
    assert ns.owns(PREFIX + "k")


def test_owns_is_false_for_another_session(ns):
    assert not ns.owns("zzz:k")


# --- key arguments ---------------------------------------------------------


def test_a_single_key_argument_is_rewritten(rewriter, ns):
    assert rewriter.rewrite(["GET", "k"], ns) == ["GET", PREFIX + "k"]


def test_the_value_is_left_alone(rewriter, ns):
    assert rewriter.rewrite(["SET", "k", "v"], ns) == ["SET", PREFIX + "k", "v"]


def test_every_key_argument_is_rewritten(rewriter, ns):
    assert rewriter.rewrite(["DEL", "a", "b"], ns) == ["DEL", PREFIX + "a", PREFIX + "b"]


def test_non_adjacent_keys_are_rewritten(rewriter, ns):
    assert rewriter.rewrite(["MSET", "a", "1", "b", "2"], ns) == [
        "MSET", PREFIX + "a", "1", PREFIX + "b", "2"
    ]


def test_a_value_equal_to_the_key_is_not_rewritten_twice(rewriter, ns):
    """SET k k must prefix the key and leave the value that looks like it."""
    assert rewriter.rewrite(["SET", "k", "k"], ns) == ["SET", PREFIX + "k", "k"]


def test_a_keyless_command_is_untouched(rewriter, ns):
    assert rewriter.rewrite(["PING"], ns) == ["PING"]


# --- patterns --------------------------------------------------------------


def test_keys_pattern_is_scoped(rewriter, ns):
    assert rewriter.rewrite(["KEYS", "*"], ns) == ["KEYS", PREFIX + "*"]


def test_scan_gets_a_match_when_none_was_given(rewriter, ns):
    assert rewriter.rewrite(["SCAN", "0"], ns)[:4] == ["SCAN", "0", "MATCH", PREFIX + "*"]


def test_scan_keeps_the_readers_pattern_scoped(rewriter, ns):
    result = rewriter.rewrite(["SCAN", "0", "MATCH", "product:*"], ns)

    assert result[3] == PREFIX + "product:*"


def test_scan_is_given_a_workable_count(rewriter, ns):
    """A small COUNT over a large keyspace returns an empty page, not no keys."""
    result = rewriter.rewrite(["SCAN", "0"], ns)

    assert result[result.index("COUNT") + 1] == "10000"


def test_a_small_reader_count_is_raised(rewriter, ns):
    result = rewriter.rewrite(["SCAN", "0", "COUNT", "10"], ns)

    assert result[result.index("COUNT") + 1] == "10000"


def test_a_large_reader_count_is_kept(rewriter, ns):
    result = rewriter.rewrite(["SCAN", "0", "COUNT", "50000"], ns)

    assert result[result.index("COUNT") + 1] == "50000"


@pytest.mark.parametrize("command", ["HSCAN", "SSCAN", "ZSCAN"])
def test_field_scans_keep_their_pattern(rewriter, ns, command):
    """These match fields inside one key; prefixing that pattern breaks them."""
    result = rewriter.rewrite([command, "k", "0", "MATCH", "f*"], ns)

    assert result == [command, PREFIX + "k", "0", "MATCH", "f*"]


# --- search indexes --------------------------------------------------------


def test_the_index_name_is_scoped(rewriter, ns):
    result = rewriter.rewrite(["FT.CREATE", "idx", "SCHEMA", "n", "TEXT"], ns)

    assert result[1] == PREFIX + "idx"


def test_a_declared_prefix_is_scoped(rewriter, ns):
    result = rewriter.rewrite(
        ["FT.CREATE", "idx", "ON", "HASH", "PREFIX", "1", "product:", "SCHEMA", "n", "TEXT"], ns
    )

    assert result[6] == PREFIX + "product:"


def test_every_declared_prefix_is_scoped(rewriter, ns):
    result = rewriter.rewrite(
        ["FT.CREATE", "idx", "PREFIX", "2", "a:", "b:", "SCHEMA", "n", "TEXT"], ns
    )

    assert result[4:6] == [PREFIX + "a:", PREFIX + "b:"]


def test_an_index_without_a_prefix_gets_one(rewriter, ns):
    """Otherwise it indexes every session's documents, and search leaks."""
    result = rewriter.rewrite(["FT.CREATE", "idx", "SCHEMA", "n", "TEXT"], ns)

    assert ["PREFIX", "1", PREFIX] == result[2:5]


def test_an_added_prefix_goes_before_the_schema(rewriter, ns):
    """Everything after SCHEMA is field definitions; a clause there is a syntax error."""
    result = rewriter.rewrite(["FT.CREATE", "idx", "SCHEMA", "n", "TEXT"], ns)

    assert result == ["FT.CREATE", PREFIX + "idx", "PREFIX", "1", PREFIX, "SCHEMA", "n", "TEXT"]


def test_an_added_prefix_keeps_the_on_clause_in_place(rewriter, ns):
    result = rewriter.rewrite(["FT.CREATE", "idx", "ON", "JSON", "SCHEMA", "$.n", "AS", "n", "TEXT"], ns)

    assert result[2:4] == ["ON", "JSON"]


def test_search_names_the_scoped_index(rewriter, ns):
    assert rewriter.rewrite(["FT.SEARCH", "idx", "q"], ns) == ["FT.SEARCH", PREFIX + "idx", "q"]


def test_dropindex_names_the_scoped_index(rewriter, ns):
    assert rewriter.rewrite(["FT.DROPINDEX", "idx"], ns) == ["FT.DROPINDEX", PREFIX + "idx"]


def test_an_alias_and_its_index_are_both_scoped(rewriter, ns):
    assert rewriter.rewrite(["FT.ALIASADD", "a", "idx"], ns) == [
        "FT.ALIASADD", PREFIX + "a", PREFIX + "idx"
    ]


def test_cursor_reads_name_the_index_one_along(rewriter, ns):
    assert rewriter.rewrite(["FT.CURSOR", "READ", "idx", "42"], ns) == [
        "FT.CURSOR", "READ", PREFIX + "idx", "42"
    ]


# --- replies ---------------------------------------------------------------


@pytest.fixture
def replies() -> ReplyFilter:
    return ReplyFilter()


def test_keys_comes_back_unprefixed(replies, ns):
    assert replies.filter(["KEYS", "*"], [PREFIX + "a", PREFIX + "b"], ns) == ["a", "b"]


def test_keys_drops_another_session(replies, ns):
    assert replies.filter(["KEYS", "*"], [PREFIX + "a", "other:b"], ns) == ["a"]


def test_scan_keeps_its_cursor(replies, ns):
    assert replies.filter(["SCAN", "0"], ["17", [PREFIX + "a"]], ns) == ["17", ["a"]]


def test_ft_list_shows_only_our_indexes(replies, ns):
    assert replies.filter(["FT._LIST"], [PREFIX + "idx", "other:idx"], ns) == ["idx"]


def test_search_unwraps_the_document_keys(replies, ns):
    reply = [1, PREFIX + "doc:1", ["n", "hello"]]

    assert replies.filter(["FT.SEARCH", "idx", "q"], reply, ns) == [1, "doc:1", ["n", "hello"]]


def test_search_leaves_the_total_alone(replies, ns):
    reply = [2, PREFIX + "doc:1", ["n", "a"], PREFIX + "doc:2", ["n", "b"]]

    assert replies.filter(["FT.SEARCH", "idx", "q"], reply, ns)[0] == 2


def test_info_unwraps_the_index_name(replies, ns):
    reply = ["index_name", PREFIX + "idx", "num_docs", 3]

    assert replies.filter(["FT.INFO", "idx"], reply, ns)[1] == "idx"


def test_multi_series_drops_another_session(replies, ns):
    reply = [[PREFIX + "ts:1", [], []], ["other:ts:2", [], []]]

    assert replies.filter(["TS.MRANGE", "-", "+"], reply, ns) == [["ts:1", [], []]]


def test_an_error_reply_is_passed_through(replies, ns):
    error = RespError("ERR no such key")

    assert replies.filter(["KEYS", "*"], error, ns) is error


def test_a_status_reply_is_passed_through(replies, ns):
    status = RespStatus("OK")

    assert replies.filter(["SET", "k", "v"], status, ns) is status


def test_an_ordinary_value_is_passed_through(replies, ns):
    assert replies.filter(["GET", "k"], "hello", ns) == "hello"


# --- when Redis cannot say where the keys are ------------------------------
#
# The two failure answers mean opposite things, and getting them the wrong way
# round writes a reader's key into the shared keyspace instead of their own.


def test_a_keyless_command_answers_with_no_keys():
    from namespace import LOOKUP_UNAVAILABLE  # noqa: F401

    resolver = KeyResolver(lambda argv: RespError("ERR The command has no key arguments"))

    assert resolver.keys_of(["PING"]) == []


def test_an_unreachable_lookup_raises_instead():
    from namespace import KeyLookupUnavailable, LOOKUP_UNAVAILABLE

    resolver = KeyResolver(lambda argv: RespError(LOOKUP_UNAVAILABLE))

    with pytest.raises(KeyLookupUnavailable):
        resolver.keys_of(["GET", "k"])


def test_a_keyless_answer_is_remembered():
    """The answer depends on the command name alone, so it never changes."""
    calls = []

    def execute(argv):
        calls.append(argv)
        return RespError("ERR The command has no key arguments")

    resolver = KeyResolver(execute)
    resolver.keys_of(["PING"])
    resolver.keys_of(["PING"])

    assert len(calls) == 1


def test_key_positions_are_never_cached():
    """They depend on argument values for EVAL, ZUNIONSTORE and GEORADIUS."""
    calls = []

    def execute(argv):
        calls.append(argv)
        return ["k"]

    resolver = KeyResolver(execute)
    resolver.keys_of(["GET", "k"])
    resolver.keys_of(["GET", "k"])

    assert len(calls) == 2
