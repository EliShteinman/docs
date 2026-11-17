"""files/git-mirrors.js: which GitHub links go to which GitLab copy, and how."""

import json
import os
import shutil
import subprocess

import pytest

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
HANDLER = os.path.join(REPO, "helm", "redis-docs", "files", "git-mirrors.js")

MIRRORS: list[dict[str, object]] = [
    {"name": "redis", "repos": ["redis/redis"], "to": "https://gl.example/g/redis"},
    {"name": "redis-py", "repos": ["redis/redis-py", "andymccurdy/redis-py"], "to": "https://gl.example/g/redis-py/"},
    {
        "name": "RedisInsight",
        "repos": ["redis/redisinsight", "redisinsight/redisinsight"],
        "to": "https://gl.example/g/ri",
    },
]

HARNESS = """
const { createTranslator } = require(process.argv[1]);
const input = JSON.parse(require('fs').readFileSync(0, 'utf8'));
const translate = createTranslator(input.mirrors);
process.stdout.write(JSON.stringify(input.hrefs.map(translate)));
"""

CASES: list[tuple[str, str | None]] = [
    ("https://github.com/redis/redis", "https://gl.example/g/redis"),
    ("https://github.com/redis/redis/", "https://gl.example/g/redis"),
    ("https://github.com/redis/redis.git", "https://gl.example/g/redis"),
    ("https://github.com/redis/redis#readme", "https://gl.example/g/redis#readme"),
    (
        "https://github.com/Redis/Redis/blob/unstable/src/t_zset.c",
        "https://gl.example/g/redis/-/blob/unstable/src/t_zset.c",
    ),
    ("http://www.github.com/redis/redis/tree/7.2/src", "https://gl.example/g/redis/-/tree/7.2/src"),
    (
        "https://github.com/redis/redis/blob/unstable/src/server.c#L10-L20",
        "https://gl.example/g/redis/-/blob/unstable/src/server.c#L10-20",
    ),
    (
        "https://github.com/redis/redis/blob/unstable/src/server.c#L10",
        "https://gl.example/g/redis/-/blob/unstable/src/server.c#L10",
    ),
    ("https://github.com/redis/redis/commit/abc123", "https://gl.example/g/redis/-/commit/abc123"),
    ("https://github.com/redis/redis/compare/7.0...7.2", "https://gl.example/g/redis/-/compare/7.0...7.2"),
    ("https://github.com/redis/redis/tags", "https://gl.example/g/redis/-/tags"),
    ("https://github.com/redis/redis/releases", "https://gl.example/g/redis/-/releases"),
    ("https://github.com/redis/redis/releases/tag/7.2.4", "https://gl.example/g/redis/-/tags/7.2.4"),
    ("https://github.com/redis/redis/releases/latest", "https://gl.example/g/redis/-/releases/permalink/latest"),
    (
        "https://github.com/redis/redis/releases/download/7.2.4/redis.tgz",
        "https://gl.example/g/redis/-/releases/7.2.4/downloads/redis.tgz",
    ),
    ("https://raw.githubusercontent.com/redis/redis/7.2/redis.conf", "https://gl.example/g/redis/-/raw/7.2/redis.conf"),
    (
        "https://raw.githubusercontent.com/redis/redis/refs/heads/unstable/redis.conf",
        "https://gl.example/g/redis/-/raw/unstable/redis.conf",
    ),
    (
        "https://github.com/redis/redis-py/blob/master/redis/client.py",
        "https://gl.example/g/redis-py/-/blob/master/redis/client.py",
    ),
    ("https://github.com/andymccurdy/redis-py", "https://gl.example/g/redis-py"),
    ("https://github.com/RedisInsight/RedisInsight/releases", "https://gl.example/g/ri/-/releases"),
    ("https://github.com/redis/RedisInsight", "https://gl.example/g/ri"),
    ("https://github.com/redis/redis-om-spring", None),
    ("https://github.com/redis/redisctl", None),
    ("https://github.com/redis/redis/pull/12345", None),
    ("https://github.com/redis/redis/issues/1", None),
    ("https://github.com/redis/redis/wiki/Page", None),
    ("https://github.com/redis/redis/security/advisories/GHSA-x", None),
    ("https://github.com/redis/redis/releases/tag", None),
    ("https://github.com/redis", None),
    ("https://gitlab.example/g/redis/-/blob/unstable/README.md", None),
    ("/docs/latest/", None),
    ("", None),
]


@pytest.fixture(scope="module")
def translated() -> dict[str, str | None]:
    if shutil.which("node") is None:
        pytest.skip("node is not installed")
    hrefs: list[str] = [href for href, _ in CASES]
    completed = subprocess.run(
        ["node", "-e", HARNESS, HANDLER],
        input=json.dumps({"mirrors": MIRRORS, "hrefs": hrefs}),
        capture_output=True,
        text=True,
        check=True,
    )
    return dict(zip(hrefs, json.loads(completed.stdout), strict=True))


@pytest.mark.parametrize(("href", "expected"), CASES)
def test_link_is_translated(translated: dict[str, str | None], href: str, expected: str | None) -> None:
    assert translated[href] == expected
