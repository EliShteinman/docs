"""Tests for the sandbox ACL — the rules in helm/redis-docs/files/sandbox.acl.

Two things can go wrong with an allowlist, and each has its own test here.

It can be too tight, and silently break a documented example: the corpus test
runs ACL DRYRUN over every real Redis command the docs demonstrate in a runnable
block, so a rule that blocks one fails here rather than in front of a reader.

It can be too loose, and let a reader reach past their own session: the deny test
names the commands that must not get through, with the reason each one matters.

Both need a live Redis with the bundled modules and the ACL file loaded, so they
skip unless docker is available. The container is started once per session:

    pytest helm/cli-proxy/test_acl.py
"""

import json
import os
import shutil
import subprocess
import sys
import time

import pytest

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "build"))

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ACL_FILE = os.path.join(REPO, "helm", "redis-docs", "files", "sandbox.acl")
CONTENT = os.path.join(REPO, "content")
IMAGE = "redis:8-alpine"
CONTAINER = "cli-proxy-acl-test"
USER = "docsandbox"

# Granted after startup by the deployment's postStart hook, because Redis parses
# the ACL file before the modules register and rejects any module command in it.
MODULE_GRANTS = ["+ft._list", "+ft.dropindex", "+ft.tagvals"]

pytestmark = pytest.mark.skipif(
    shutil.which("docker") is None, reason="needs docker to run a real Redis"
)


def redis(*args: str) -> str:
    result = subprocess.run(
        ["docker", "exec", CONTAINER, "redis-cli", *args],
        capture_output=True,
        text=True,
    )
    return (result.stdout + result.stderr).strip()


@pytest.fixture(scope="session")
def sandbox() -> None:
    """A Redis running the real ACL file, set up the way the chart sets it up."""
    subprocess.run(["docker", "rm", "-f", CONTAINER], capture_output=True)
    started = subprocess.run(
        [
            "docker", "run", "-d", "--rm", "--name", CONTAINER,
            "-v", f"{ACL_FILE}:/etc/redis/sandbox.acl:ro",
            IMAGE, "redis-server", "--aclfile", "/etc/redis/sandbox.acl",
        ],
        capture_output=True,
        text=True,
    )
    if started.returncode != 0:
        pytest.skip(f"could not start {IMAGE}: {started.stderr.strip()}")

    for _ in range(30):
        if redis("PING") == "PONG":
            break
        time.sleep(1)
    else:
        subprocess.run(["docker", "rm", "-f", CONTAINER], capture_output=True)
        pytest.skip("redis did not come up — check the ACL file parses")

    redis("ACL", "SETUSER", USER, *MODULE_GRANTS)
    yield
    subprocess.run(["docker", "rm", "-f", CONTAINER], capture_output=True)


def permits(command: str) -> bool:
    """Whether the sandbox user may run this command.

    DRYRUN answers "OK", a NOPERM message, or an arity complaint — and an arity
    complaint means the permission check already passed, so it counts as allowed.
    """
    verdict = redis("ACL", "DRYRUN", USER, *command.split())
    return verdict == "OK" or "arguments" in verdict.lower()


def demonstrated_commands() -> list[str]:
    """Every real Redis command the docs show in a runnable CLI example."""
    from components.cli_parser import extract_cli_commands

    real = {name.strip().upper() for name in redis("COMMAND", "LIST").splitlines() if name.strip()}

    found: set[str] = set()
    for root, _, files in os.walk(CONTENT):
        for name in files:
            if not name.endswith(".md"):
                continue
            with open(os.path.join(root, name), encoding="utf-8", errors="replace") as handle:
                text = handle.read()
            if "> " not in text:
                continue
            for command in extract_cli_commands(text):
                if command.split()[0].upper() in real:
                    found.add(command.upper())
    return sorted(found)


# Commands the docs demonstrate that the rules block on purpose. Each one edits
# or reports on the server itself, which is not a reader's to do.
DELIBERATELY_BLOCKED = {"ACL LIST", "ACL LOAD", "ACL SAVE", "DEBUG OBJECT", "ROLE", "SLOWLOG RESET"}

# What a reader must not be able to reach, and why it matters.
MUST_DENY = [
    ("FLUSHALL", "wipes the keyspace every other visitor is working in"),
    ("FLUSHDB async", "the same, one database down"),
    ("SWAPDB 0 1", "swaps a whole database out from under everyone"),
    ("SELECT 1", "escapes the database the session is confined to"),
    ("RANDOMKEY", "hands back a key belonging to someone else's session"),
    ("MIGRATE host 6379 k 0 100", "moves keys off the sandbox entirely"),
    ("DUMP k", "serializes any key, straight past the proxy"),
    ("RESTORE k 0 payload", "injects a key the proxy never saw"),
    ("CONFIG GET maxmemory", "reads and writes server configuration"),
    ("DEBUG OBJECT k", "server internals"),
    ("SHUTDOWN NOSAVE", "stops Redis"),
    ("MONITOR", "streams every other visitor's commands"),
    ("CLIENT KILL ID 1", "reaches into other connections"),
    ("SUBSCRIBE channel", "wedges a sticky session in subscribe mode"),
    ("PSUBSCRIBE pattern", "the same"),
    ("REPLICAOF host 6379", "repoints replication"),
    ("SAVE", "blocks the server on a synchronous dump"),
    ("ACL SETUSER other on", "rewrites the permissions this file sets"),
    ("SCRIPT FLUSH", "discards every cached script, everyone's"),
]

# What has to keep working, including the two the postStart hook grants back.
MUST_PERMIT = [
    "GET k", "SET k v", "DEL k", "TYPE k", "TTL k", "EXPIRE k 1",
    "KEYS *", "SCAN 0", "INFO keyspace", "DBSIZE", "PING",
    "MULTI", "EXEC", "DISCARD", "WATCH k",
    "HSET k f v", "ZADD k 1 m", "XADD k * f v", "EVAL script 0", "PUBLISH ch m",
    "FT.CREATE i SCHEMA n TEXT", "FT.SEARCH i q", "FT._LIST", "FT.DROPINDEX i",
    "JSON.SET k $ 1", "TS.CREATE k", "BF.ADD k v",
    "COMMAND GETKEYS GET k",
]


def test_redis_starts_with_the_acl_file(sandbox):
    assert redis("PING") == "PONG"


def test_the_sandbox_user_exists(sandbox):
    assert USER in redis("ACL", "USERS").split()


@pytest.mark.parametrize("command,reason", MUST_DENY, ids=[c.split()[0] for c, _ in MUST_DENY])
def test_denied(sandbox, command, reason):
    assert not permits(command), f"{command} is reachable, and it {reason}"


@pytest.mark.parametrize("command", MUST_PERMIT, ids=lambda c: c.split()[0])
def test_permitted(sandbox, command):
    assert permits(command), f"{command} is blocked, and the docs rely on it"


def test_the_docs_corpus_still_runs(sandbox):
    """No documented example is blocked except the ones we meant to block."""
    blocked = {c for c in demonstrated_commands() if not permits(c)}

    assert blocked == DELIBERATELY_BLOCKED


def test_default_user_is_left_open_for_the_probes(sandbox):
    """The liveness probe and the Jupyter sidecar both connect with no credentials."""
    assert redis("ACL", "DRYRUN", "default", "PING") == "OK"


def test_reset_cannot_be_denied_by_acl(sandbox):
    """Why main.py has to refuse RESET itself: no ACL rule reaches it.

    If this ever fails, Redis has made RESET deniable and PROXY_DENIED can go.
    """
    redis("ACL", "SETUSER", USER, "-reset")

    assert redis("ACL", "DRYRUN", USER, "RESET") == "OK"
