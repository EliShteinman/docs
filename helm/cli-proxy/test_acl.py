"""Tests for the sandbox ACL — the rules in helm/redis-docs/files/sandbox.acl.

Two things can go wrong with an allowlist, and each has its own test here.

It can be too tight, and break a Try it button: the Try it test runs ACL DRYRUN
over every command line a reader can run from the docs, so a rule that blocks
one fails here rather than in front of a reader.

It can be too loose, and let a reader reach past their own session: the deny test
names the commands that must not get through, with the reason each one matters.

Both need a live Redis with the bundled modules and the ACL file loaded, so they
skip unless docker is available. The container is started once per session:

    pytest helm/cli-proxy/test_acl.py
"""

import json
import os
import shlex
import shutil
import subprocess
import sys
import time

import pytest

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

from command_catalog import CommandCatalog  # noqa: E402
from sandbox_acl import MODULE_GRANTS, PROXY_DENIED, SandboxAcl  # noqa: E402
from source_tree import WorkingTree  # noqa: E402
from try_it import DELIBERATELY_BLOCKED, SHORTCODE_NAMES, try_it_lines  # noqa: E402

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ACL_FILE = os.path.join(REPO, "helm", "redis-docs", "files", "sandbox.acl")
IMAGE = "redis:8-alpine"
CONTAINER = "cli-proxy-acl-test"
USER = "docsandbox"

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


def refuses(command_line: str) -> bool:
    """Whether the ACL turns this exact line away.

    Checked with its own arguments: DRYRUN tests arity before permissions, so a
    bare "HOTKEYS START" answers with an arity complaint and looks allowed.
    """
    try:
        argv = shlex.split(command_line)
    except ValueError:
        argv = command_line.split()
    return "no permissions" in redis("ACL", "DRYRUN", USER, *argv).lower()


def try_it_commands() -> list[tuple[str, str]]:
    """Every Try it command line in the docs, with the command it runs."""
    tree = WorkingTree(REPO)
    catalog = CommandCatalog.from_pages(list(tree.markdown("content/commands").values()))
    commands: set[tuple[str, str]] = set()
    for text in tree.markdown("content", containing=SHORTCODE_NAMES).values():
        for line in try_it_lines(text):
            name = catalog.resolve(line)
            if name:
                commands.add((line, name))
    return sorted(commands)


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
    "COMMAND GETKEYS GET k", "ROLE",
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


def test_every_try_it_still_runs(sandbox):
    """No Try it command is blocked except the ones redis.io blocks too."""
    blocked = {name for line, name in try_it_commands() if refuses(line)}

    assert blocked == DELIBERATELY_BLOCKED


def test_the_merge_gate_reads_the_acl_as_redis_does(sandbox):
    """helm/tools/try_it_gate.py judges the ACL from the docs alone; hold it to Redis.

    PROXY_DENIED is left out: the proxy refuses those, where DRYRUN cannot see.
    """
    tree = WorkingTree(REPO)
    catalog = CommandCatalog.from_pages(list(tree.markdown("content/commands").values()))
    with open(ACL_FILE, encoding="utf-8") as handle:
        acl = SandboxAcl.from_acl_file(handle.read(), USER)

    disagreements = {
        line for line, name in try_it_commands()
        if name not in PROXY_DENIED and acl.allows(name, catalog.categories(name)) == refuses(line)
    }

    assert not disagreements


def test_default_user_is_left_open_for_the_probes(sandbox):
    """The liveness probe connects with no credentials."""
    assert redis("ACL", "DRYRUN", "default", "PING") == "OK"


def test_reset_cannot_be_denied_by_acl(sandbox):
    """Why main.py has to refuse RESET itself: no ACL rule reaches it.

    If this ever fails, Redis has made RESET deniable and PROXY_DENIED can go.
    """
    redis("ACL", "SETUSER", USER, "-reset")

    assert redis("ACL", "DRYRUN", USER, "RESET") == "OK"
