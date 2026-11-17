from collections.abc import Callable
from pathlib import Path

import pytest

from airgap_mirrors.git import BareRepository, GitRunner
from tests.support.upstream import UpstreamRepository, git

pytestmark = pytest.mark.integration


@pytest.fixture
def upstream(make_upstream: Callable[..., UpstreamRepository]) -> UpstreamRepository:
    repository: UpstreamRepository = make_upstream(default_branch="unstable")
    repository.commit("release/7.2", "fix.txt", "fix")
    repository.tag("7.2.0")
    return repository


@pytest.fixture
def copy(tmp_path: Path, upstream: UpstreamRepository) -> BareRepository:
    repository: BareRepository = BareRepository(tmp_path / "copy.git", GitRunner())
    repository.create()
    repository.track_upstream(upstream.bare.as_uri())
    repository.fetch_upstream()
    return repository


@pytest.fixture
def receiver(tmp_path: Path) -> BareRepository:
    repository: BareRepository = BareRepository(tmp_path / "receiver.git", GitRunner())
    repository.create()
    return repository


def test_copy_holds_upstream_branches_and_tags(copy: BareRepository, upstream: UpstreamRepository) -> None:
    assert copy.branch_and_tag_tips() == upstream.refs()


def test_copy_skips_pull_request_refs(tmp_path: Path, upstream: UpstreamRepository) -> None:
    upstream.pull_request_ref(1, upstream.refs()["refs/heads/unstable"])
    repository: BareRepository = BareRepository(tmp_path / "fresh.git", GitRunner())
    repository.create()
    repository.track_upstream(upstream.bare.as_uri())
    repository.fetch_upstream()
    assert "refs/pull/1/head" not in git("for-each-ref", "--format=%(refname)", cwd=repository.path)


def test_stray_refs_are_dropped(copy: BareRepository) -> None:
    git("update-ref", "refs/pull/9/head", "refs/heads/unstable", cwd=copy.path)
    copy.drop_refs_outside_branches_and_tags()
    assert "refs/pull/9/head" not in git("for-each-ref", "--format=%(refname)", cwd=copy.path)


def test_upstream_default_branch_is_read_from_the_remote(copy: BareRepository) -> None:
    assert copy.upstream_default_branch() == "unstable"


def test_upstream_default_branch_change_is_seen(copy: BareRepository, upstream: UpstreamRepository) -> None:
    upstream.set_default_branch("release/7.2")
    assert copy.upstream_default_branch() == "release/7.2"


def test_delta_has_nothing_new_when_only_a_lightweight_tag_moved(
    copy: BareRepository, upstream: UpstreamRepository
) -> None:
    known: list[str] = sorted(copy.branch_and_tag_tips().values())
    upstream.tag("light", annotated=False)
    copy.fetch_upstream()
    assert copy.has_objects_beyond(["refs/tags/light"], known) is False


def test_delta_has_new_objects_after_a_commit(copy: BareRepository, upstream: UpstreamRepository) -> None:
    known: list[str] = sorted(copy.branch_and_tag_tips().values())
    upstream.commit("unstable", "new.txt", "new")
    copy.fetch_upstream()
    assert copy.has_objects_beyond(["refs/heads/unstable"], known) is True


def test_full_bundle_rebuilds_every_ref(tmp_path: Path, copy: BareRepository, receiver: BareRepository) -> None:
    tips: dict[str, str] = copy.branch_and_tag_tips()
    bundle: Path = tmp_path / "full.bundle"
    copy.create_bundle(bundle, sorted(tips), [])
    receiver.unpack_bundle(bundle)
    receiver.set_branches_and_tags(tips)
    assert receiver.branch_and_tag_tips() == tips


def test_delta_bundle_applies_on_top_of_the_full_one(
    tmp_path: Path, copy: BareRepository, receiver: BareRepository, upstream: UpstreamRepository
) -> None:
    first: dict[str, str] = copy.branch_and_tag_tips()
    copy.create_bundle(tmp_path / "full.bundle", sorted(first), [])
    receiver.unpack_bundle(tmp_path / "full.bundle")
    receiver.set_branches_and_tags(first)
    upstream.commit("unstable", "next.txt", "next")
    copy.fetch_upstream()
    second: dict[str, str] = copy.branch_and_tag_tips()
    copy.create_bundle(tmp_path / "delta.bundle", ["refs/heads/unstable"], sorted(first.values()))
    receiver.verify_bundle(tmp_path / "delta.bundle")
    receiver.unpack_bundle(tmp_path / "delta.bundle")
    receiver.set_branches_and_tags(second)
    assert receiver.branch_and_tag_tips() == second


def test_unpacking_leaves_no_temporary_refs(tmp_path: Path, copy: BareRepository, receiver: BareRepository) -> None:
    tips: dict[str, str] = copy.branch_and_tag_tips()
    copy.create_bundle(tmp_path / "full.bundle", sorted(tips), [])
    receiver.unpack_bundle(tmp_path / "full.bundle")
    assert receiver.branch_and_tag_tips() == {}


def test_missing_objects_are_reported(copy: BareRepository, receiver: BareRepository) -> None:
    wanted: set[str] = set(copy.branch_and_tag_tips().values())
    assert receiver.missing_objects(wanted) == wanted


def test_setting_refs_removes_the_ones_not_listed(copy: BareRepository) -> None:
    tips: dict[str, str] = copy.branch_and_tag_tips()
    kept: dict[str, str] = {name: object_id for name, object_id in tips.items() if name != "refs/heads/release/7.2"}
    copy.set_branches_and_tags(kept)
    assert copy.branch_and_tag_tips() == kept


def test_prune_push_deletes_remote_branches_gone_locally(copy: BareRepository, receiver: BareRepository) -> None:
    refspecs: list[str] = ["+refs/heads/*:refs/heads/*", "+refs/tags/*:refs/tags/*"]
    copy.push(receiver.path.as_uri(), refspecs, prune=True)
    tips: dict[str, str] = copy.branch_and_tag_tips()
    copy.set_branches_and_tags({name: value for name, value in tips.items() if name != "refs/heads/release/7.2"})
    copy.push(receiver.path.as_uri(), refspecs, prune=True)
    assert "refs/heads/release/7.2" not in receiver.branch_and_tag_tips()
