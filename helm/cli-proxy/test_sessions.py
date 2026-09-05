"""Tests for the session registry and the sandbox login.

The registry is the part of the proxy with state that outlives a request, so
these cover the two ways a session goes away — idle timeout and the cap — plus
the reuse that everything else depends on. RespConnection is faked: what matters
here is which connections get closed and when, not the RESP wire.
"""

import os
import sys
import threading

import pytest

sys.path.insert(0, os.path.dirname(__file__))

from resp import RespError
from sessions import RedisAuthError, Session, SessionRegistry, authenticate


class FakeConnection:
    """Stands in for RespConnection, recording what was sent and what to reply."""

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


@pytest.fixture
def connections() -> list[FakeConnection]:
    return []


@pytest.fixture
def connect(connections):
    def _connect() -> FakeConnection:
        connection = FakeConnection()
        connections.append(connection)
        return connection

    return _connect


@pytest.fixture
def registry(connect) -> SessionRegistry:
    """A registry that never sweeps on its own, so tests drive the clock."""
    return SessionRegistry(connect, max_sessions=3, idle_ttl=100.0, sweep_interval=0.0)


def test_acquire_without_id_mints_one(registry):
    _, sid = registry.acquire(None)

    assert sid


def test_acquire_reuses_the_same_session(registry):
    first, sid = registry.acquire(None)
    second, _ = registry.acquire(sid)

    assert second is first


def test_reuse_does_not_open_a_second_connection(registry, connections):
    _, sid = registry.acquire(None)
    registry.acquire(sid)

    assert len(connections) == 1


def test_each_new_session_opens_its_own_connection(registry, connections):
    registry.acquire(None)
    registry.acquire(None)

    assert len(connections) == 2


def test_discard_closes_the_connection(registry):
    session, sid = registry.acquire(None)
    registry.discard(sid)

    assert session.connection.closed


def test_discard_forgets_the_session(registry):
    _, sid = registry.acquire(None)
    registry.discard(sid)

    assert len(registry) == 0


def test_discard_of_an_unknown_id_is_a_no_op(registry):
    registry.discard("never-existed")

    assert len(registry) == 0


def test_cap_holds_the_session_count(registry):
    for _ in range(5):
        registry.acquire(None)

    assert len(registry) == 3


def test_cap_closes_what_it_evicts(registry):
    evicted, _ = registry.acquire(None)
    for _ in range(3):
        registry.acquire(None)

    assert evicted.connection.closed


def test_cap_evicts_the_least_recently_used(registry):
    oldest, oldest_sid = registry.acquire(None)
    _, keep_sid = registry.acquire(None)
    registry.acquire(keep_sid)  # touch, so `oldest` is now the stalest
    registry.acquire(None)
    registry.acquire(None)

    assert oldest.connection.closed


def test_cap_spares_the_session_that_was_touched(registry):
    registry.acquire(None)
    kept, keep_sid = registry.acquire(None)
    registry.acquire(keep_sid)
    registry.acquire(None)
    registry.acquire(None)

    assert not kept.connection.closed


def test_cap_leaves_a_session_that_is_mid_batch(registry):
    busy, _ = registry.acquire(None)
    busy.lock.acquire()
    try:
        for _ in range(4):
            registry.acquire(None)
    finally:
        busy.lock.release()

    assert not busy.connection.closed


def test_sweep_closes_an_idle_session(registry):
    idle, _ = registry.acquire(None)
    idle.last_seen -= 200.0
    registry.sweep()

    assert idle.connection.closed


def test_sweep_forgets_an_idle_session(registry):
    idle, _ = registry.acquire(None)
    idle.last_seen -= 200.0
    registry.sweep()

    assert len(registry) == 0


def test_sweep_keeps_a_session_inside_the_timeout(registry):
    fresh, _ = registry.acquire(None)
    fresh.last_seen -= 50.0
    registry.sweep()

    assert not fresh.connection.closed


def test_sweep_stops_at_the_first_live_session(registry):
    idle, _ = registry.acquire(None)
    idle.last_seen -= 200.0
    fresh, _ = registry.acquire(None)
    registry.sweep()

    assert not fresh.connection.closed


def test_sweep_leaves_a_session_that_is_mid_batch(registry):
    busy, _ = registry.acquire(None)
    busy.last_seen -= 200.0
    busy.lock.acquire()
    try:
        registry.sweep()
    finally:
        busy.lock.release()

    assert not busy.connection.closed


def test_a_zero_cap_still_leaves_the_new_session_usable(connect):
    registry = SessionRegistry(connect, max_sessions=0, idle_ttl=100.0, sweep_interval=0.0)
    session, _ = registry.acquire(None)

    assert not session.connection.closed


def test_sweep_honours_its_interval(connect):
    registry = SessionRegistry(connect, max_sessions=10, idle_ttl=0.0, sweep_interval=3600.0)
    session, _ = registry.acquire(None)
    registry.sweep()

    assert not session.connection.closed


def test_acquire_is_safe_under_concurrent_callers(connect):
    registry = SessionRegistry(connect, max_sessions=50, idle_ttl=100.0, sweep_interval=0.0)
    sessions = []
    barrier = threading.Barrier(8)

    def race() -> None:
        barrier.wait()
        sessions.append(registry.acquire("shared-id")[0])

    threads = [threading.Thread(target=race) for _ in range(8)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert len(set(id(session) for session in sessions)) == 1


def test_losing_a_connect_race_closes_the_spare(connect, connections):
    registry = SessionRegistry(connect, max_sessions=50, idle_ttl=100.0, sweep_interval=0.0)
    barrier = threading.Barrier(4)

    def race() -> None:
        barrier.wait()
        registry.acquire("shared-id")

    threads = [threading.Thread(target=race) for _ in range(4)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert sum(1 for connection in connections if not connection.closed) == 1


# --- authentication -------------------------------------------------------
#
# A connection that stays on Redis's default user runs a reader's commands with
# full rights, so these pin down that a refused AUTH ends the connection rather
# than falling through to one that can still run FLUSHALL.


def test_auth_sends_the_credentials():
    connection = FakeConnection()
    authenticate(connection, "docsandbox", "")

    assert connection.sent == [["AUTH", "docsandbox", ""]]


def test_auth_leaves_an_accepted_connection_open():
    connection = FakeConnection()
    authenticate(connection, "docsandbox", "")

    assert not connection.closed


def test_a_refused_auth_raises():
    connection = FakeConnection([RespError("WRONGPASS invalid username-password pair")])

    with pytest.raises(RedisAuthError):
        authenticate(connection, "docsandbox", "nope")


def test_a_refused_auth_closes_the_connection():
    connection = FakeConnection([RespError("WRONGPASS invalid username-password pair")])

    with pytest.raises(RedisAuthError):
        authenticate(connection, "docsandbox", "nope")

    assert connection.closed
