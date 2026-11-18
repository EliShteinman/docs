from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import MagicMock, call

import pytest
from pydantic import SecretStr
from pytest_mock import MockerFixture

from airgap_mirrors.exceptions import MissingObjectsError
from airgap_mirrors.external import ExportOutcome, GitExporter
from airgap_mirrors.git import BareRepository
from airgap_mirrors.internal import GitImporter, GitLabClient, GitLabProject, ProjectProvisioner
from airgap_mirrors.models import ExportLedger, ImportLedger, RepositoryState, TransferManifest
from airgap_mirrors.settings import ExternalRepoSpec, ExternalSettings, InternalRepoSpec, InternalSettings
from airgap_mirrors.storage import JsonModelStore, LedgerLocator
from airgap_mirrors.transfer import TransferLayout

MOMENT: datetime = datetime(2026, 1, 1, tzinfo=UTC)
STATE: RepositoryState = RepositoryState(
    default_branch="unstable", refs={"refs/heads/unstable": "c2", "refs/tags/v1": "t1"}
)
EXTERNAL_SPEC: ExternalRepoSpec = ExternalRepoSpec(name="redis", github="redis/redis")
INTERNAL_SPEC: InternalRepoSpec = InternalRepoSpec(name="redis", gitlab_path="g/redis")


class FixedClock:
    def now(self) -> datetime:
        return MOMENT


@pytest.fixture
def repository(mocker: MockerFixture) -> MagicMock:
    mock: MagicMock = mocker.create_autospec(BareRepository, instance=True)
    mock.exists.return_value = True
    mock.upstream_default_branch.return_value = STATE.default_branch
    mock.branch_and_tag_tips.return_value = dict(STATE.refs)
    mock.has_object.return_value = True
    mock.has_objects_beyond.return_value = True
    mock.missing_objects.return_value = set()
    mock.create_bundle.side_effect = lambda path, *_: (
        path.parent.mkdir(parents=True, exist_ok=True),
        path.write_bytes(b"x"),
    )
    return mock


@pytest.fixture
def exporter(tmp_path: Path, repository: MagicMock) -> GitExporter:
    settings: ExternalSettings = ExternalSettings(
        mirrors_dir=tmp_path / "m",
        transfer_dir=tmp_path / "t",
        github_url="https://github.com",
        github_api_url="https://api.github.com",
        http_timeout_seconds=5,
        download_attempts=1,
        default_assets="none",
        repos=[EXTERNAL_SPEC],
    )
    return GitExporter(
        settings,
        lambda _: repository,
        TransferLayout(tmp_path / "t"),
        LedgerLocator(tmp_path / "m"),
        JsonModelStore(),
        FixedClock(),
    )


def confirm(tmp_path: Path, state: RepositoryState) -> None:
    JsonModelStore().save(LedgerLocator(tmp_path / "m").export_ledger("redis"), ExportLedger(confirmed=state))


def test_first_export_bundles_every_ref(exporter: GitExporter, repository: MagicMock) -> None:
    exporter.export(EXTERNAL_SPEC)
    assert repository.create_bundle.call_args.args[1:] == (["refs/heads/unstable", "refs/tags/v1"], [])


def test_new_repository_copy_is_created(exporter: GitExporter, repository: MagicMock) -> None:
    repository.exists.return_value = False
    exporter.export(EXTERNAL_SPEC)
    repository.create.assert_called_once_with()


def test_head_follows_the_upstream_default(exporter: GitExporter, repository: MagicMock) -> None:
    exporter.export(EXTERNAL_SPEC)
    repository.point_head_at.assert_called_once_with("unstable")


def test_export_is_skipped_when_nothing_changed(exporter: GitExporter, tmp_path: Path) -> None:
    confirm(tmp_path, STATE)
    assert exporter.export(EXTERNAL_SPEC) is ExportOutcome.UNCHANGED


def test_default_branch_change_alone_is_exported(exporter: GitExporter, repository: MagicMock, tmp_path: Path) -> None:
    confirm(tmp_path, STATE.model_copy(update={"default_branch": "main"}))
    assert exporter.export(EXTERNAL_SPEC) is ExportOutcome.REFS_ONLY


def test_delta_excludes_what_gitlab_already_has(exporter: GitExporter, repository: MagicMock, tmp_path: Path) -> None:
    confirm(
        tmp_path, RepositoryState(default_branch="unstable", refs={"refs/heads/unstable": "c1", "refs/tags/v1": "t1"})
    )
    exporter.export(EXTERNAL_SPEC)
    assert repository.create_bundle.call_args.args[1:] == (["refs/heads/unstable"], ["c1", "t1"])


def test_refs_without_new_objects_write_no_bundle(exporter: GitExporter, repository: MagicMock, tmp_path: Path) -> None:
    confirm(tmp_path, RepositoryState(default_branch="unstable", refs={"refs/heads/unstable": "c2"}))
    repository.has_objects_beyond.return_value = False
    assert exporter.export(EXTERNAL_SPEC) is ExportOutcome.REFS_ONLY


def test_full_export_ignores_the_confirmed_state(exporter: GitExporter, tmp_path: Path) -> None:
    confirm(tmp_path, STATE)
    assert exporter.export(EXTERNAL_SPEC, full=True) is ExportOutcome.BUNDLED


def test_export_leaves_the_state_pending(exporter: GitExporter, tmp_path: Path) -> None:
    exporter.export(EXTERNAL_SPEC)
    ledger: ExportLedger | None = JsonModelStore().load(
        LedgerLocator(tmp_path / "m").export_ledger("redis"), ExportLedger
    )
    assert STATE.state_id in (ledger.pending if ledger else {})


def test_manifest_names_its_bundle(exporter: GitExporter, tmp_path: Path) -> None:
    exporter.export(EXTERNAL_SPEC)
    layout: TransferLayout = TransferLayout(tmp_path / "t")
    manifest: TransferManifest | None = JsonModelStore().load(layout.manifest_path("redis", MOMENT), TransferManifest)
    assert (manifest.bundle_file if manifest else None) == layout.bundle_path("redis", MOMENT).name


@pytest.fixture
def gitlab(mocker: MockerFixture) -> MagicMock:
    client: MagicMock = mocker.create_autospec(GitLabClient, instance=True)
    client.project.return_value = GitLabProject(id=1, path_with_namespace="g/redis", default_branch="main")
    return client


@pytest.fixture
def staged_layout(tmp_path: Path) -> TransferLayout:
    layout: TransferLayout = TransferLayout(tmp_path / "t")
    JsonModelStore().save(
        layout.manifest_path("redis", MOMENT),
        TransferManifest(name="redis", upstream_url="u", state=STATE, bundle_file="b.bundle", created_at=MOMENT),
    )
    return layout


@pytest.fixture
def provisioner(mocker: MockerFixture, gitlab: MagicMock) -> MagicMock:
    mock: MagicMock = mocker.create_autospec(ProjectProvisioner, instance=True)
    mock.ensure_project.side_effect = lambda spec, _url: gitlab.project(spec.gitlab_path)
    return mock


@pytest.fixture
def importer(
    tmp_path: Path, repository: MagicMock, gitlab: MagicMock, provisioner: MagicMock, staged_layout: TransferLayout
) -> GitImporter:
    settings: InternalSettings = InternalSettings(
        mirrors_dir=tmp_path / "m",
        transfer_dir=tmp_path / "t",
        gitlab_url="https://gl",
        gitlab_group="g",
        release_package_name="p",
        http_timeout_seconds=5,
        GITLAB_TOKEN=SecretStr("x"),
        repos=[INTERNAL_SPEC],
    )
    return GitImporter(
        settings,
        lambda _: repository,
        staged_layout,
        LedgerLocator(tmp_path / "m"),
        JsonModelStore(),
        gitlab,
        provisioner,
    )


def test_import_without_transfers_touches_nothing(importer: GitImporter, gitlab: MagicMock, tmp_path: Path) -> None:
    for path in (tmp_path / "t").rglob("*.json"):
        path.unlink()
    importer.import_repository(INTERNAL_SPEC)
    gitlab.project.assert_not_called()


def test_import_makes_sure_the_project_exists(importer: GitImporter, provisioner: MagicMock) -> None:
    importer.import_repository(INTERNAL_SPEC)
    provisioner.ensure_project.assert_called_once_with(INTERNAL_SPEC, "u")


def test_import_reports_the_project_address(importer: GitImporter, gitlab: MagicMock) -> None:
    gitlab.project.return_value = GitLabProject(id=1, path_with_namespace="g/redis", web_url="https://gl/g/redis")
    assert importer.import_repository(INTERNAL_SPEC).project_url == "https://gl/g/redis"


def test_import_builds_the_address_when_gitlab_gives_none(importer: GitImporter) -> None:
    assert importer.import_repository(INTERNAL_SPEC).project_url == "https://gl/g/redis"


def test_import_pushes_the_default_branch_first_then_everything(importer: GitImporter, repository: MagicMock) -> None:
    importer.import_repository(INTERNAL_SPEC)
    url: str = "https://gl/g/redis.git"
    assert repository.push.call_args_list == [
        call(url, ["+refs/heads/unstable:refs/heads/unstable"]),
        call(url, ["+refs/heads/*:refs/heads/*", "+refs/tags/*:refs/tags/*"], prune=True),
    ]


def test_import_sets_the_gitlab_default_branch(importer: GitImporter, gitlab: MagicMock) -> None:
    importer.import_repository(INTERNAL_SPEC)
    gitlab.set_default_branch.assert_called_once_with("g/redis", "unstable")


def test_import_leaves_a_correct_default_branch_alone(importer: GitImporter, gitlab: MagicMock) -> None:
    gitlab.project.return_value = GitLabProject(id=1, path_with_namespace="g/redis", default_branch="unstable")
    importer.import_repository(INTERNAL_SPEC)
    gitlab.set_default_branch.assert_not_called()


def test_import_refuses_a_transfer_missing_its_base(importer: GitImporter, repository: MagicMock) -> None:
    repository.missing_objects.return_value = {"c1"}
    with pytest.raises(MissingObjectsError):
        importer.import_repository(INTERNAL_SPEC)


def test_import_skips_a_transfer_already_applied(importer: GitImporter, repository: MagicMock, tmp_path: Path) -> None:
    JsonModelStore().save(
        LedgerLocator(tmp_path / "m").import_ledger("redis"), ImportLedger(applied_state_ids=[STATE.state_id])
    )
    importer.import_repository(INTERNAL_SPEC)
    repository.unpack_bundle.assert_not_called()


def test_import_returns_the_applied_states(importer: GitImporter) -> None:
    assert importer.import_repository(INTERNAL_SPEC).state_ids == [STATE.state_id]


def test_import_unprotects_an_old_default_gone_upstream(importer: GitImporter, gitlab: MagicMock) -> None:
    gitlab.project.return_value = GitLabProject(id=1, path_with_namespace="g/redis", default_branch="v1-branch")
    importer.import_repository(INTERNAL_SPEC)
    gitlab.unprotect_branch.assert_called_once_with("g/redis", "v1-branch")


def test_import_unprotects_nothing_for_a_new_project(importer: GitImporter, gitlab: MagicMock) -> None:
    gitlab.project.return_value = GitLabProject(id=1, path_with_namespace="g/redis", default_branch=None)
    importer.import_repository(INTERNAL_SPEC)
    gitlab.unprotect_branch.assert_not_called()
