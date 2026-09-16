"""End-to-end: a real index in a real Redis, and what a reader gets back.

Every other test here drives a fake connection and checks the commands that
were sent. That proves the wiring and nothing about the answers: the weights,
the title bonus, the version multiplier, BM25 over DIALECT 2 and the
single-character prefix are all decisions the query engine acts on, and a fake
will agree with whatever the code does. The claims in config.py and query.py --
that a command's own page outranks the reference pages listing it, that a
current page outranks its copy in an old version -- were measured by hand
against a real index and had nothing holding them.

This builds a small index the same way the pod does, from a feed in the shape
build/generate_ndjson.py writes, and asks it the questions those claims answer.

Needs docker, like test_acl.py, and uses the same image so a run pulls one:

    pytest helm/cli-proxy/search/test_search_live.py
"""

import json
import os
import shutil
import subprocess
import sys
import time

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from search import config, indexer, main, query

IMAGE = "redis:8-alpine"
CONTAINER = "search-live-test"
PORT = 16395

pytestmark = pytest.mark.skipif(
    shutil.which("docker") is None, reason="needs docker to run a real Redis"
)

# A page for each claim under test. The bodies are what separates them: the
# reference page mentions every command once, so a search for one of them
# matches it as well as the command's own page.
FEED = [
    {
        "url": "/commands/set/",
        "title": "SET",
        "summary": "Set the string value of a key.",
        "sections": [{"title": "Options", "text": "EX sets an expiry in seconds."}],
        "version": "latest",
    },
    {
        "url": "/commands/",
        "title": "Commands reference",
        "summary": "Every command Redis accepts.",
        "sections": [
            {
                "title": "Strings",
                "text": "SET SETEX SETNX SETRANGE GETSET MSET MSETNX APPEND SET SET SET",
            }
        ],
        "version": "latest",
    },
    {
        "url": "/commands/json.set/",
        "title": "JSON.SET",
        "summary": "Set the JSON value at a path.",
        "sections": [{"title": "Examples", "text": "Store a document at the root."}],
        "version": "latest",
    },
    {
        "url": "/operate/rs/rack-zone-awareness/",
        "title": "Rack-zone awareness",
        "summary": "Spread shards across racks.",
        "sections": [{"title": "Setup", "text": "Enable rack awareness per cluster."}],
        "version": "latest",
    },
    {
        "url": "/operate/rs/7.4/rack-zone-awareness/",
        "title": "Rack-zone awareness",
        "summary": "Spread shards across racks.",
        "sections": [{"title": "Setup", "text": "Enable rack awareness per cluster."}],
        "version": "7.4",
    },
    {
        # The highest-numbered version tree there is. It outranks 7.4 below
        # it and still loses to the page above, which carries no version at
        # all: the unversioned tree IS the current release -- for Redis
        # Software that is 8.2, whose release notes publish only there -- and
        # the numbered trees are the archive behind it, in their own order.
        "url": "/operate/rs/8.0/rack-zone-awareness/",
        "title": "Rack-zone awareness",
        "summary": "Spread shards across racks.",
        "sections": [{"title": "Setup", "text": "Enable rack awareness per cluster."}],
        "version": "8.0",
    },
    {
        "url": "/operate/kubernetes/scaling/",
        "title": "Scale a database",
        "summary": "Add shards to a database on Kubernetes.",
        "sections": [{"title": "Shards", "text": "Resharding moves slots between nodes."}],
        "version": "latest",
    },
    {
        "url": "/develop/active-active/",
        "title": "Active-Active geo-distribution",
        "summary": "Write to any replica of an Active-Active database.",
        "sections": [{"title": "Conflicts", "text": "CRDTs resolve concurrent writes."}],
        "version": "latest",
    },
    {
        "url": "/blog/vector-search-explained/",
        "title": "Vector search explained",
        "summary": "A post about vector search.",
        "sections": [{"title": "Why", "text": "Embeddings turn meaning into numbers."}],
        "version": "latest",
    },
]


def redis_cli(*args: str) -> str:
    result = subprocess.run(
        ["docker", "exec", CONTAINER, "redis-cli", *args], capture_output=True, text=True
    )
    return (result.stdout + result.stderr).strip()


@pytest.fixture(scope="module")
def live_index(tmp_path_factory, request):
    """A Redis holding an index built from FEED, with the service pointed at it."""
    subprocess.run(["docker", "rm", "-f", CONTAINER], capture_output=True)
    started = subprocess.run(
        ["docker", "run", "-d", "--rm", "--name", CONTAINER, "-p", f"{PORT}:6379", IMAGE],
        capture_output=True,
        text=True,
    )
    if started.returncode != 0:
        pytest.skip(f"could not start {IMAGE}: {started.stderr.strip()}")

    for _ in range(30):
        if redis_cli("PING") == "PONG":
            break
        time.sleep(1)
    else:
        subprocess.run(["docker", "rm", "-f", CONTAINER], capture_output=True)
        pytest.skip("redis did not come up")

    feed = tmp_path_factory.mktemp("corpus") / "docs.ndjson"
    feed.write_text("\n".join(json.dumps(record) for record in FEED), encoding="utf-8")

    # The pod configures the service through the environment; here the same
    # values are set on the module the service reads them from, so the index is
    # built and queried exactly as indexer.main() would.
    for name, value in (
        ("REDIS_HOST", "127.0.0.1"),
        ("REDIS_PORT", PORT),
        ("DOCS_FEED_PATH", str(feed)),
        ("INDEX_NAME", "docs_live_test"),
        ("KEY_PREFIX", "live_test_doc:"),
    ):
        request.addfinalizer(
            lambda name=name, previous=getattr(config, name): setattr(config, name, previous)
        )
        setattr(config, name, value)

    written = indexer.build_index()
    assert written == len(FEED)
    request.addfinalizer(main.CONNECTIONS.discard)
    yield
    subprocess.run(["docker", "rm", "-f", CONTAINER], capture_output=True)


def search(term: str, product: str = "all", **paging) -> dict:
    body, status = main.run_search(
        term,
        product,
        paging.get("limit", config.RESULT_LIMIT),
        paging.get("offset", 0),
    )
    assert status == 200, body
    return body


def plain(text: str) -> str:
    """A title without the marks the service puts around the matched words."""
    return text.replace(query.HIGHLIGHT_OPEN, "").replace(query.HIGHLIGHT_CLOSE, "")


def titles(body: dict) -> list[str]:
    return [plain(result["title"]) for result in body["results"]]


def test_the_index_answers_at_all(live_index):
    assert titles(search("rack*"))


def test_a_commands_own_page_outranks_the_reference_page_listing_it(live_index):
    """The title bonus in query.py, which a prefix alone does not give."""
    assert titles(search("set*"))[0] == "SET"


def test_a_dotted_command_name_is_found_by_its_own_name(live_index):
    """`json.set` is indexed as two terms, so the query has to split the same way."""
    assert "JSON.SET" in titles(search("json.set*"))


def test_a_hyphenated_name_is_not_read_as_an_exclusion(live_index):
    """Left bare, `Active-Active` asks the parser for "Active, excluding Active"."""
    assert "Active-Active geo-distribution" in titles(search("active-active*"))


def test_one_letter_answers_rather_than_waiting_for_a_second(live_index):
    """MINPREFIX 1: the modal fires on the first keystroke."""
    assert titles(search("r*"))


def test_the_unversioned_page_wins_over_every_numbered_copy(live_index):
    """config.VERSION_WEIGHT, and the row the modal draws links to the winner.

    Including the highest-numbered one: the current documentation is the tree
    with no version in its path, and 8.0 is ranked down exactly like 7.4.
    """
    results = search("rack*")["results"]
    rack = [result for result in results if plain(result["title"]) == "Rack-zone awareness"]
    assert len(rack) == 1, "the modal keys rows by title; only the best copy may be sent"
    assert rack[0]["url"] == "/operate/rs/rack-zone-awareness/"
    assert rack[0]["version"] == "latest"


def test_the_archive_keeps_its_own_order_under_the_current_page(live_index):
    """Newer archived versions answer ahead of older ones, all behind `latest`."""
    scores = {
        document.get("version"): float(document[query.SCORE_KEY])
        for document in query.parse_reply(_raw("rack*"))[1]
    }
    assert scores["latest"] > scores["8.0"] > scores["7.4"]


def test_an_old_version_is_still_reachable_when_asked_for(live_index):
    """A multiplier, not a filter: the numbered copies are ranked down, not hidden."""
    _, documents = query.parse_reply(_raw("rack*"))
    versions = [document.get("version") for document in documents]
    assert "7.4" in versions and "8.0" in versions


def _raw(term: str) -> object:
    """The unfiltered reply, before one_per_row drops the duplicate rows."""
    from resp import RespConnection

    connection = RespConnection(config.REDIS_HOST, config.REDIS_PORT, config.SOCKET_TIMEOUT)
    try:
        connection.send_command(
            query.search_command(config.INDEX_NAME, query.build_query(term, "all"), 30)
        )
        return connection.read_reply()
    finally:
        connection.close()


def test_the_product_filter_selects_by_the_second_path_segment(live_index):
    assert titles(search("database*", product="kubernetes")) == ["Scale a database"]


def test_an_unknown_product_answers_nothing_rather_than_failing(live_index):
    assert search("set*", product="banana") == {"total": 0, "results": []}


def test_a_result_says_which_body_of_content_it_came_from(live_index):
    post = search("embeddings*")["results"][0]
    assert post["source"] == "blog"
    assert post["hierarchy"][0] != config.ROOT_CRUMB, "a blog post is not documentation"


def test_a_result_carries_a_score_a_caller_can_compare(live_index):
    results = search("set*")["results"]
    assert results[0]["score"] > 0
    assert results[0]["score"] >= results[-1]["score"]


def test_the_matched_words_come_back_marked_in_the_body(live_index):
    assert "<b>" in search("embeddings*")["results"][0]["body"]


def test_a_page_size_limits_what_comes_back(live_index):
    assert len(search("set*", limit=1)["results"]) == 1


def test_paging_moves_past_the_first_result(live_index):
    first = search("set*", limit=1)["results"][0]["url"]
    second = search("set*", limit=1, offset=1)["results"][0]["url"]
    assert first != second


def test_the_total_counts_every_match_not_just_the_page(live_index):
    body = search("set*", limit=1)
    assert body["total"] > len(body["results"])
