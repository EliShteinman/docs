from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from pydantic import SecretStr
from pytest_mock import MockerFixture

from airgap_mirrors.commands import ExportCommand, ImportCommand, RepositoryBatch
from airgap_mirrors.exceptions import ConfigurationError, GitCommandError, TransferError
from airgap_mirrors.external import GitExporter, ReleaseExporter
from airgap_mirrors.internal import GitImporter, HelmValuesWriter, ImportResult, ReleaseImporter
from airgap_mirrors.settings import ExternalRepoSpec, InternalRepoSpec, InternalSettings
from airgap_mirrors.storage import JsonModelStore, LedgerLocator
from airgap_mirrors.transfer import TransferLayout

MOMENT: datetime = datetime(2026, 1, 1, tzinfo=UTC)
A: InternalRepoSpec = InternalRepoSpec(name="a", gitlab_path="g/a")
B: InternalRepoSpec = InternalRepoSpec(name="b", gitlab_path="g/b")


class FixedClock:
    def now(self) -> datetime:
        return MOMENT


def test_batch_keeps_going_after_a_failure() -> None:
    seen: list[str] = []

    def step(spec: InternalRepoSpec) -> None:
        seen.append(spec.name)
        if spec.name == "a":
            raise GitCommandError(["push"], 1, "rejected")

    assert (RepositoryBatch().run("push", [A, B], step), seen) == (["a"], ["a", "b"])


def test_export_runs_releases_after_git(mocker: MockerFixture) -> None:
    git: MagicMock = mocker.create_autospec(GitExporter, instance=True)
    releases: MagicMock = mocker.create_autospec(ReleaseExporter, instance=True)
    spec: ExternalRepoSpec = ExternalRepoSpec(name="a", github="o/a")
    ExportCommand(git, releases, RepositoryBatch()).run([spec], full=True)
    assert (git.export.call_args.kwargs, releases.export.call_args.kwargs) == ({"full": True}, {"full": True})


def imported(spec: InternalRepoSpec) -> ImportResult:
    return ImportResult(state_ids=[f"{spec.name}-state"], project_url=f"https://gl/{spec.gitlab_path}")


@pytest.fixture
def import_parts(mocker: MockerFixture, tmp_path: Path) -> tuple[MagicMock, MagicMock, TransferLayout]:
    git: MagicMock = mocker.create_autospec(GitImporter, instance=True)
    git.import_repository.side_effect = imported
    releases: MagicMock = mocker.create_autospec(ReleaseImporter, instance=True)
    layout: TransferLayout = TransferLayout(tmp_path / "t")
    for name in ("a", "b"):
        layout.git_dir(name).mkdir(parents=True)
    return git, releases, layout


def run_import(parts: tuple[MagicMock, MagicMock, TransferLayout], wanted: list[str] | None = None) -> list[str]:
    git, releases, layout = parts
    settings: InternalSettings = InternalSettings(
        mirrors_dir=layout.root.parent / "m",
        transfer_dir=layout.root,
        gitlab_url="https://gl",
        gitlab_group="g",
        release_package_name="p",
        http_timeout_seconds=5,
        GITLAB_TOKEN=SecretStr("x"),
    )
    ledgers: LedgerLocator = LedgerLocator(settings.mirrors_dir)
    helm: HelmValuesWriter = HelmValuesWriter(ledgers.published_projects, ledgers.helm_values, JsonModelStore())
    command: ImportCommand = ImportCommand(settings, git, releases, helm, RepositoryBatch(), layout)
    return command.run(wanted or [])


def test_import_finds_the_repositories_in_the_transfer_folder(
    import_parts: tuple[MagicMock, MagicMock, TransferLayout],
) -> None:
    run_import(import_parts)
    assert [item.args[0].gitlab_path for item in import_parts[0].import_repository.call_args_list] == ["g/a", "g/b"]


def test_import_can_be_narrowed_to_one_repository(import_parts: tuple[MagicMock, MagicMock, TransferLayout]) -> None:
    run_import(import_parts, ["b"])
    assert [item.args[0].name for item in import_parts[0].import_repository.call_args_list] == ["b"]


def test_import_refuses_a_repository_the_folder_lacks(
    import_parts: tuple[MagicMock, MagicMock, TransferLayout],
) -> None:
    with pytest.raises(ConfigurationError, match="nope"):
        run_import(import_parts, ["nope"])


def test_import_writes_helm_values_for_the_imported_projects(
    import_parts: tuple[MagicMock, MagicMock, TransferLayout],
) -> None:
    run_import(import_parts)
    values: str = (import_parts[2].root.parent / "m" / "helm-values-git-mirrors.yaml").read_text()
    assert '    "b":\n      enabled: true\n      to: "https://gl/g/b"' in values


def test_import_skips_releases_of_a_repository_whose_git_failed(
    import_parts: tuple[MagicMock, MagicMock, TransferLayout],
) -> None:
    git, releases, _ = import_parts
    git.import_repository.side_effect = [TransferError("bad"), ImportResult(state_ids=["b-state"])]
    run_import(import_parts)
    assert [item.args[0].name for item in releases.import_repository.call_args_list] == ["b"]
