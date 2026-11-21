import shutil
from collections.abc import Callable

import pytest

from airgap_mirrors.commands import ExportCommand, ImportCommand
from airgap_mirrors.composition import Composition
from airgap_mirrors.exceptions import ConfigurationError, TransferError
from airgap_mirrors.external import ExportOutcome, GitExporter
from airgap_mirrors.internal import GitImporter
from airgap_mirrors.models import TransferManifest
from airgap_mirrors.settings import ExternalRepoSpec, ExternalSettings, InternalRepoSpec, InternalSettings
from tests.conftest import SteppingClock
from tests.support.fake_servers import FakeGitLab, FakeProject
from tests.support.upstream import UpstreamRepository, git

pytestmark = pytest.mark.integration

GITLAB_PATH: str = "mirrors/redis/widget"


class Cycle:
    """One online machine, one air-gapped machine, one USB folder between them."""

    def __init__(self, composition: Composition, online: ExternalSettings, airgap: InternalSettings) -> None:
        self.online: ExternalSettings = online
        self.airgap: InternalSettings = airgap
        self._composition: Composition = composition

    def export(self, *, full: bool = False) -> list[str]:
        command: ExportCommand = self._composition.export_command(self.online, with_releases=False)
        return command.run(self.online.repos, full=full)

    def import_(self) -> list[str]:
        command: ImportCommand = self._composition.import_command(self.airgap, with_releases=False)
        return command.run([])

    def exporter(self) -> GitExporter:
        return self._composition.git_exporter(self.online)

    def importer(self) -> GitImporter:
        return self._composition.git_importer(self.airgap)

    def round_trip(self) -> None:
        assert self.export() == []
        assert self.import_() == []

    def clear_usb(self) -> None:
        for path in sorted(self.online.transfer_dir.rglob("*"), reverse=True):
            path.unlink() if path.is_file() else path.rmdir()


@pytest.fixture
def upstream(make_upstream: Callable[..., UpstreamRepository]) -> UpstreamRepository:
    repository: UpstreamRepository = make_upstream(default_branch="unstable")
    repository.commit("7.2", "fix.txt", "fix")
    repository.tag("7.2.0")
    return repository


@pytest.fixture
def project(gitlab_server: FakeGitLab) -> FakeProject:
    return gitlab_server.add_project(GITLAB_PATH)


@pytest.fixture
def cycle(
    clock: SteppingClock,
    upstream: UpstreamRepository,
    project: FakeProject,
    external_settings: Callable[..., ExternalSettings],
    internal_settings: Callable[..., InternalSettings],
) -> Cycle:
    online: ExternalSettings = external_settings([ExternalRepoSpec(name="widget", github="acme/widget")])
    airgap: InternalSettings = internal_settings([InternalRepoSpec(name="widget", gitlab_path=GITLAB_PATH)])
    return Cycle(Composition(clock=clock), online, airgap)


def gitlab_refs(project: FakeProject) -> dict[str, str]:
    output: str = git("for-each-ref", "--format=%(objectname) %(refname)", cwd=project.repository)
    return {name: object_id for object_id, name in (line.split(" ", 1) for line in output.splitlines())}


def test_first_transfer_copies_every_branch_and_tag(
    cycle: Cycle, upstream: UpstreamRepository, project: FakeProject
) -> None:
    cycle.round_trip()
    assert gitlab_refs(project) == upstream.refs()


def test_first_transfer_keeps_the_upstream_default_branch(cycle: Cycle, project: FakeProject) -> None:
    cycle.round_trip()
    assert project.default_branch == "unstable"


def test_second_export_without_changes_writes_nothing(cycle: Cycle) -> None:
    cycle.round_trip()
    cycle.clear_usb()
    cycle.export()
    assert not list(cycle.online.transfer_dir.rglob("*.manifest.json"))


def test_second_transfer_carries_new_commits(cycle: Cycle, upstream: UpstreamRepository, project: FakeProject) -> None:
    cycle.round_trip()
    cycle.clear_usb()
    upstream.commit("unstable", "next.txt", "next")
    cycle.round_trip()
    assert gitlab_refs(project) == upstream.refs()


def test_new_tag_on_an_old_branch_is_carried_while_default_branch_is_idle(
    cycle: Cycle, upstream: UpstreamRepository, project: FakeProject
) -> None:
    cycle.round_trip()
    cycle.clear_usb()
    upstream.commit("7.2", "fix2.txt", "fix2")
    upstream.tag("7.2.1")
    cycle.round_trip()
    assert gitlab_refs(project)["refs/tags/7.2.1"] == upstream.refs()["refs/tags/7.2.1"]


def test_branch_deleted_upstream_is_deleted_in_gitlab(
    cycle: Cycle, upstream: UpstreamRepository, project: FakeProject
) -> None:
    cycle.round_trip()
    cycle.clear_usb()
    upstream.delete_branch("7.2")
    cycle.round_trip()
    assert "refs/heads/7.2" not in gitlab_refs(project)


def test_default_branch_renamed_upstream_follows_in_gitlab(
    cycle: Cycle, upstream: UpstreamRepository, project: FakeProject
) -> None:
    cycle.round_trip()
    cycle.clear_usb()
    upstream.commit("main", "main.txt", "main")
    upstream.set_default_branch("main")
    upstream.delete_branch("unstable")
    cycle.round_trip()
    assert project.default_branch == "main"


def test_old_default_loses_its_gitlab_protection_when_renamed_upstream(
    cycle: Cycle, upstream: UpstreamRepository, project: FakeProject
) -> None:
    cycle.round_trip()
    cycle.clear_usb()
    project.protected.add("unstable")
    upstream.commit("main", "main.txt", "main")
    upstream.set_default_branch("main")
    upstream.delete_branch("unstable")
    cycle.round_trip()
    assert "unstable" not in project.protected


def test_refs_only_transfer_has_no_bundle(cycle: Cycle, upstream: UpstreamRepository) -> None:
    cycle.round_trip()
    cycle.clear_usb()
    upstream.tag("light", annotated=False)
    cycle.export()
    assert not list(cycle.online.transfer_dir.rglob("*.bundle"))


def test_full_export_ignores_what_was_sent(cycle: Cycle) -> None:
    cycle.round_trip()
    cycle.clear_usb()
    cycle.export(full=True)
    assert list(cycle.online.transfer_dir.rglob("*.bundle"))


def forget_the_airgap_copy(cycle: Cycle) -> None:
    shutil.rmtree(cycle.airgap.mirrors_dir)


def test_fresh_machine_applies_a_delta_bundle_on_what_gitlab_holds(
    cycle: Cycle, upstream: UpstreamRepository, project: FakeProject
) -> None:
    cycle.round_trip()
    cycle.clear_usb()
    upstream.commit("unstable", "x.txt", "x")
    cycle.export()
    forget_the_airgap_copy(cycle)
    cycle.import_()
    assert gitlab_refs(project) == upstream.refs()


def test_fresh_machine_applies_a_refs_only_transfer_on_what_gitlab_holds(
    cycle: Cycle, upstream: UpstreamRepository, project: FakeProject
) -> None:
    cycle.round_trip()
    cycle.clear_usb()
    upstream.tag("light", annotated=False)
    cycle.export()
    forget_the_airgap_copy(cycle)
    cycle.import_()
    assert gitlab_refs(project) == upstream.refs()


@pytest.fixture
def fresh_cycle(
    clock: SteppingClock,
    upstream: UpstreamRepository,
    gitlab_server: FakeGitLab,
    external_settings: Callable[..., ExternalSettings],
    internal_settings: Callable[..., InternalSettings],
) -> Cycle:
    gitlab_server.add_group("redis")
    online: ExternalSettings = external_settings([ExternalRepoSpec(name="widget", github="acme/widget")])
    return Cycle(Composition(clock=clock), online, internal_settings(group="redis/mirrors"))


def test_missing_project_is_created_in_the_group(fresh_cycle: Cycle, gitlab_server: FakeGitLab) -> None:
    fresh_cycle.round_trip()
    assert "redis/mirrors/widget" in gitlab_server.projects


def test_missing_subgroup_is_created_on_the_way(fresh_cycle: Cycle, gitlab_server: FakeGitLab) -> None:
    fresh_cycle.round_trip()
    assert "redis/mirrors" in gitlab_server.groups


def test_created_project_gets_the_upstream_default_branch(fresh_cycle: Cycle, gitlab_server: FakeGitLab) -> None:
    fresh_cycle.round_trip()
    assert gitlab_server.projects["redis/mirrors/widget"].default_branch == "unstable"


def test_created_project_carries_everything_upstream_has(
    fresh_cycle: Cycle, gitlab_server: FakeGitLab, upstream: UpstreamRepository
) -> None:
    fresh_cycle.round_trip()
    assert gitlab_refs(gitlab_server.projects["redis/mirrors/widget"]) == upstream.refs()


@pytest.mark.parametrize(
    "setting",
    ["issues_access_level", "merge_requests_access_level", "wiki_access_level", "snippets_access_level"],
)
def test_created_project_is_a_plain_copy(fresh_cycle: Cycle, gitlab_server: FakeGitLab, setting: str) -> None:
    fresh_cycle.round_trip()
    assert gitlab_server.projects["redis/mirrors/widget"].created_with[setting] == "disabled"


def test_created_project_starts_empty(fresh_cycle: Cycle, gitlab_server: FakeGitLab) -> None:
    fresh_cycle.round_trip()
    assert gitlab_server.projects["redis/mirrors/widget"].created_with["initialize_with_readme"] is False


def test_second_import_reuses_the_project(
    fresh_cycle: Cycle, gitlab_server: FakeGitLab, upstream: UpstreamRepository
) -> None:
    fresh_cycle.round_trip()
    fresh_cycle.clear_usb()
    upstream.commit("unstable", "more.txt", "more")
    fresh_cycle.round_trip()
    assert len(gitlab_server.projects) == 1


def test_missing_top_group_fails_with_a_clear_message(
    clock: SteppingClock,
    upstream: UpstreamRepository,
    external_settings: Callable[..., ExternalSettings],
    internal_settings: Callable[..., InternalSettings],
) -> None:
    online: ExternalSettings = external_settings([ExternalRepoSpec(name="widget", github="acme/widget")])
    cycle: Cycle = Cycle(Composition(clock=clock), online, internal_settings(group="nowhere"))
    cycle.export()
    with pytest.raises(ConfigurationError, match="no group 'nowhere'"):
        cycle.importer().import_repository(cycle.airgap.spec_for("widget"))


def test_export_again_before_the_transfer_writes_nothing_new(cycle: Cycle) -> None:
    cycle.export()
    cycle.export()
    assert len(list(cycle.online.transfer_dir.rglob("*.bundle"))) == 1


def test_export_with_nothing_new_writes_nothing(cycle: Cycle) -> None:
    cycle.round_trip()
    cycle.clear_usb()
    assert cycle.exporter().export(cycle.online.repos[0]) is ExportOutcome.UNCHANGED


def test_each_export_carries_only_what_came_after_the_previous_one(cycle: Cycle, upstream: UpstreamRepository) -> None:
    cycle.export()
    upstream.commit("unstable", "later.txt", "later")
    cycle.export()
    first, second = (
        TransferManifest.model_validate_json(path.read_text())
        for path in sorted(cycle.online.transfer_dir.rglob("*.manifest.json"))
    )
    assert second.base_state_id == first.state.state_id


def test_transfers_imported_one_by_one_arrive_whole(
    cycle: Cycle, upstream: UpstreamRepository, project: FakeProject
) -> None:
    cycle.round_trip()
    cycle.clear_usb()
    upstream.commit("unstable", "later.txt", "later")
    cycle.round_trip()
    assert gitlab_refs(project) == upstream.refs()


def test_transfers_imported_together_arrive_whole(
    cycle: Cycle, upstream: UpstreamRepository, project: FakeProject
) -> None:
    cycle.export()
    upstream.commit("unstable", "later.txt", "later")
    cycle.export()
    cycle.import_()
    assert gitlab_refs(project) == upstream.refs()


def test_lost_transfer_is_reported_by_the_next_import(cycle: Cycle, upstream: UpstreamRepository) -> None:
    cycle.round_trip()
    cycle.clear_usb()
    upstream.commit("unstable", "lost.txt", "lost")
    cycle.export()
    cycle.clear_usb()
    upstream.commit("unstable", "next.txt", "next")
    cycle.export()
    with pytest.raises(TransferError, match="--full"):
        cycle.importer().import_repository(cycle.airgap.spec_for("widget"))


def test_full_export_recovers_from_a_lost_transfer(
    cycle: Cycle, upstream: UpstreamRepository, project: FakeProject
) -> None:
    cycle.round_trip()
    cycle.clear_usb()
    upstream.commit("unstable", "lost.txt", "lost")
    cycle.export()
    cycle.clear_usb()
    cycle.export(full=True)
    cycle.import_()
    assert gitlab_refs(project) == upstream.refs()


def test_fresh_machine_keeps_applying_later_transfers(
    cycle: Cycle, upstream: UpstreamRepository, project: FakeProject
) -> None:
    cycle.round_trip()
    cycle.clear_usb()
    upstream.commit("unstable", "x.txt", "x")
    cycle.export()
    forget_the_airgap_copy(cycle)
    cycle.import_()
    cycle.clear_usb()
    upstream.commit("unstable", "y.txt", "y")
    cycle.round_trip()
    assert gitlab_refs(project) == upstream.refs()
