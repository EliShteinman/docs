"""End-to-end: two readers, one Redis, and no sight of each other.

Everything else is a unit test of one rewriting rule. This is the claim those
rules exist to support — that two people working through the same tutorial, in
the same database, writing the same key names, do not collide — checked by
driving the real Flask app against a real Redis with the real ACL file.

Needs docker. The container is started once for the session.
"""

import json
import os
import shutil
import subprocess
import sys
import time

import pytest

sys.path.insert(0, os.path.dirname(__file__))

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ACL_FILE = os.path.join(REPO, "helm", "redis-docs", "files", "sandbox.acl")
IMAGE = "redis:8-alpine"
CONTAINER = "cli-proxy-isolation-test"
PORT = "16394"

pytestmark = pytest.mark.skipif(
    shutil.which("docker") is None, reason="needs docker to run a real Redis"
)


@pytest.fixture(scope="session")
def client():
    """The proxy, wired to a throwaway Redis running the real ACL file."""
    subprocess.run(["docker", "rm", "-f", CONTAINER], capture_output=True)
    started = subprocess.run(
        [
            "docker", "run", "-d", "--rm", "--name", CONTAINER,
            "-p", f"{PORT}:6379",
            "-v", f"{ACL_FILE}:/etc/redis/sandbox.acl:ro",
            IMAGE, "redis-server", "--aclfile", "/etc/redis/sandbox.acl",
        ],
        capture_output=True,
        text=True,
    )
    if started.returncode != 0:
        pytest.skip(f"could not start {IMAGE}: {started.stderr.strip()}")

    for _ in range(30):
        probe = subprocess.run(
            ["docker", "exec", CONTAINER, "redis-cli", "PING"], capture_output=True, text=True
        )
        if probe.stdout.strip() == "PONG":
            break
        time.sleep(1)
    else:
        subprocess.run(["docker", "rm", "-f", CONTAINER], capture_output=True)
        pytest.skip("redis did not come up")

    subprocess.run(
        ["docker", "exec", CONTAINER, "redis-cli", "ACL", "SETUSER", "docsandbox",
         "+ft._list", "+ft.dropindex", "+ft.tagvals"],
        capture_output=True,
    )

    # Point the proxy at this container by setting the values rather than
    # re-importing it. Reloading the modules would give this file its own copies
    # of RespStatus and friends, and an isinstance check in main would then stop
    # recognising the classes another test file passes it.
    import config
    import main

    config.REDIS_PORT = int(PORT)
    config.REDIS_USERNAME = "docsandbox"
    main._registry._sweep_interval = 0.0
    main._registry._idle_ttl = 100000.0

    yield main.app.test_client()
    subprocess.run(["docker", "rm", "-f", CONTAINER], capture_output=True)


class Reader:
    """One browser session, keeping its id across calls the way cli.js does."""

    def __init__(self, client) -> None:
        self._client = client
        self.sid = None

    def run(self, *commands: str) -> list:
        body = {"commands": list(commands), "id": self.sid}
        payload = self._client.post("/cli", json=body).get_json()
        self.sid = payload["id"]
        return [reply.get("value") for reply in payload["replies"]]

    def one(self, command: str):
        return self.run(command)[0]


@pytest.fixture
def alice(client) -> Reader:
    return Reader(client)


@pytest.fixture
def bob(client) -> Reader:
    return Reader(client)


# --- the collision this whole thing exists to prevent ----------------------


def test_two_readers_hold_different_values_at_the_same_key(alice, bob):
    alice.one("SET product:1 alice")
    bob.one("SET product:1 bob")

    assert alice.one("GET product:1") == "alice"


def test_the_second_writer_keeps_their_own_value(alice, bob):
    alice.one("SET product:1 alice")
    bob.one("SET product:1 bob")

    assert bob.one("GET product:1") == "bob"


def test_a_reader_cannot_see_the_others_key(alice, bob):
    alice.one("SET secret hello")

    assert bob.one("GET secret") is None


def test_a_reader_cannot_delete_the_others_key(alice, bob):
    alice.one("SET durable hello")
    bob.one("DEL durable")

    assert alice.one("GET durable") == "hello"


# --- what the reader is shown ----------------------------------------------


def test_keys_shows_the_name_the_reader_typed(alice):
    alice.one("SET product:1 v")

    assert alice.one("KEYS *") == ["product:1"]


def test_keys_shows_nothing_of_the_other_session(alice, bob):
    alice.one("SET mine v")
    bob.one("SET theirs v")

    assert "theirs" not in alice.one("KEYS *")


def test_scan_finds_the_readers_keys(alice):
    alice.one("SET scanned v")

    assert "scanned" in alice.one("SCAN 0")[1]


def test_scan_with_a_small_count_still_finds_them(alice):
    """The floor on COUNT is why this returns anything at all."""
    alice.one("SET tiny v")

    assert "tiny" in alice.one("SCAN 0 COUNT 1")[1]


def test_an_error_never_shows_the_session_prefix(alice):
    """Redis quotes the key it was given; the reader must not see the namespace."""
    alice.one("SET str hello")

    assert alice.sid not in str(alice.one("LPUSH str x"))


# --- search ----------------------------------------------------------------


def test_a_search_finds_the_readers_own_document(alice):
    alice.run(
        "FT.CREATE items ON HASH PREFIX 1 item: SCHEMA name TEXT",
        "HSET item:1 name apple",
    )
    time.sleep(0.3)

    assert alice.one("FT.SEARCH items apple")[0] == 1


def test_a_search_returns_the_key_the_reader_typed(alice):
    alice.run(
        "FT.CREATE named ON HASH PREFIX 1 thing: SCHEMA name TEXT",
        "HSET thing:1 name pear",
    )
    time.sleep(0.3)

    assert alice.one("FT.SEARCH named pear")[1] == "thing:1"


def test_a_search_does_not_reach_the_other_session(alice, bob):
    alice.run(
        "FT.CREATE shared ON HASH PREFIX 1 doc: SCHEMA name TEXT",
        "HSET doc:1 name alicedoc",
    )
    bob.run(
        "FT.CREATE shared ON HASH PREFIX 1 doc: SCHEMA name TEXT",
        "HSET doc:1 name bobdoc",
    )
    time.sleep(0.3)

    assert alice.one("FT.SEARCH shared bobdoc")[0] == 0


def test_two_readers_may_use_the_same_index_name(alice, bob):
    """The same name in two sessions is two indexes, so neither reader is refused."""
    alice.one("FT.CREATE dup SCHEMA n TEXT")

    assert bob.one("FT.CREATE dup SCHEMA n TEXT") == "OK"


def test_ft_list_shows_the_name_the_reader_typed(alice):
    alice.one("FT.CREATE listed SCHEMA n TEXT")

    assert "listed" in alice.one("FT._LIST")


def test_ft_list_hides_the_other_session(alice, bob):
    alice.one("FT.CREATE alices SCHEMA n TEXT")
    bob.one("FT.CREATE bobs SCHEMA n TEXT")

    assert "bobs" not in alice.one("FT._LIST")


def test_an_index_created_without_a_prefix_stays_in_its_session(alice, bob):
    """FT.CREATE with no PREFIX would otherwise index everybody's keys."""
    alice.one("FT.CREATE bare SCHEMA name TEXT")
    bob.one("HSET loose name bobonly")
    time.sleep(0.3)

    assert alice.one("FT.SEARCH bare bobonly")[0] == 0


# --- transactions still work ------------------------------------------------


def test_a_transaction_spanning_requests_commits(alice):
    alice.one("MULTI")
    alice.one("SET tx 1")
    alice.one("EXEC")

    assert alice.one("GET tx") == "1"


def test_a_transaction_writes_into_the_session(alice, bob):
    alice.one("MULTI")
    alice.one("SET txscoped alice")
    alice.one("EXEC")

    assert bob.one("GET txscoped") is None


# --- the ACL is still in front of all of it ---------------------------------


def test_flushall_is_refused(alice):
    assert "NOPERM" in str(alice.one("FLUSHALL"))


def test_a_refused_flushall_leaves_the_keys(alice):
    alice.one("SET survivor v")
    alice.one("FLUSHALL")

    assert alice.one("GET survivor") == "v"


def test_reset_is_refused(alice):
    assert "no permissions" in str(alice.one("RESET"))


# --- cleanup ----------------------------------------------------------------


def test_a_reclaimed_session_takes_its_keys_with_it(client, alice):
    import main

    alice.one("SET temporary v")
    sid = alice.sid
    main._registry._idle_ttl = 0.0
    main._registry._last_sweep = 0.0
    main._registry.sweep()

    left = subprocess.run(
        ["docker", "exec", CONTAINER, "redis-cli", "KEYS", f"{sid}:*"],
        capture_output=True, text=True,
    ).stdout.strip()

    assert left == ""


def test_a_reclaimed_session_takes_its_indexes_with_it(client, bob):
    import main

    bob.one("FT.CREATE doomed SCHEMA n TEXT")
    sid = bob.sid
    main._registry._idle_ttl = 0.0
    main._registry._last_sweep = 0.0
    main._registry.sweep()

    listed = subprocess.run(
        ["docker", "exec", CONTAINER, "redis-cli", "FT._LIST"],
        capture_output=True, text=True,
    ).stdout

    assert f"{sid}:doomed" not in listed
