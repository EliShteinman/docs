import pytest

from airgap_mirrors.models import ExportLedger, ImportLedger, RepositoryState


@pytest.fixture
def state() -> RepositoryState:
    return RepositoryState(default_branch="main", refs={"refs/heads/main": "a1", "refs/tags/v1": "b2"})


def test_state_id_is_stable_for_the_same_content(state: RepositoryState) -> None:
    assert state.state_id == RepositoryState(default_branch="main", refs=dict(reversed(state.refs.items()))).state_id


def test_state_id_changes_with_the_default_branch(state: RepositoryState) -> None:
    assert state.state_id != state.model_copy(update={"default_branch": "unstable"}).state_id


def test_every_ref_is_new_without_a_base(state: RepositoryState) -> None:
    assert state.refs_changed_since(None) == ["refs/heads/main", "refs/tags/v1"]


def test_only_moved_and_new_refs_count_as_changed(state: RepositoryState) -> None:
    base: RepositoryState = RepositoryState(
        default_branch="main", refs={"refs/heads/main": "a1", "refs/tags/v1": "old"}
    )
    assert state.refs_changed_since(base) == ["refs/tags/v1"]


def test_object_ids_are_the_ref_tips(state: RepositoryState) -> None:
    assert state.object_ids() == {"a1", "b2"}


def test_pending_state_is_recorded(state: RepositoryState) -> None:
    assert ExportLedger().with_pending(state).pending == {state.state_id: state}


def test_confirming_promotes_the_pending_state(state: RepositoryState) -> None:
    assert ExportLedger().with_pending(state).with_confirmed(state.state_id).confirmed == state


def test_confirming_clears_that_pending_entry(state: RepositoryState) -> None:
    assert ExportLedger().with_pending(state).with_confirmed(state.state_id).pending == {}


def test_applying_twice_records_once() -> None:
    assert ImportLedger().with_applied("x").with_applied("x").applied_state_ids == ["x"]
