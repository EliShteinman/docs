from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from airgap_mirrors.commands import ConfirmCommand, ExportCommand, ImportCommand, RepositoryBatch
from airgap_mirrors.exceptions import GitCommandError, TransferError
from airgap_mirrors.external import GitExporter, ReceiptConfirmer, ReleaseExporter
from airgap_mirrors.internal import GitImporter, ReleaseImporter
from airgap_mirrors.models import ExportLedger, ImportedState, ImportReceipt, RepositoryState
from airgap_mirrors.settings import ExternalRepoSpec, InternalRepoSpec
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
    assert (git.export.call_args.kwargs, releases.export.call_args.args) == ({"full": True}, (spec,))


@pytest.fixture
def import_parts(mocker: MockerFixture, tmp_path: Path) -> tuple[MagicMock, MagicMock, TransferLayout]:
    git: MagicMock = mocker.create_autospec(GitImporter, instance=True)
    git.import_repository.side_effect = lambda spec: [f"{spec.name}-state"]
    releases: MagicMock = mocker.create_autospec(ReleaseImporter, instance=True)
    return git, releases, TransferLayout(tmp_path)


def run_import(parts: tuple[MagicMock, MagicMock, TransferLayout]) -> list[str]:
    git, releases, layout = parts
    return ImportCommand(git, releases, RepositoryBatch(), layout, JsonModelStore(), FixedClock()).run([A, B])


def test_import_writes_a_receipt_of_every_applied_state(
    import_parts: tuple[MagicMock, MagicMock, TransferLayout],
) -> None:
    run_import(import_parts)
    receipt: ImportReceipt | None = JsonModelStore().load(import_parts[2].receipt_path, ImportReceipt)
    assert [entry.state_id for entry in (receipt.entries if receipt else [])] == ["a-state", "b-state"]


def test_import_skips_releases_of_a_repository_whose_git_failed(
    import_parts: tuple[MagicMock, MagicMock, TransferLayout],
) -> None:
    git, releases, _ = import_parts
    git.import_repository.side_effect = [TransferError("bad"), ["b-state"]]
    run_import(import_parts)
    assert [item.args[0].name for item in releases.import_repository.call_args_list] == ["b"]


@pytest.fixture
def confirmer_parts(tmp_path: Path) -> tuple[ReceiptConfirmer, LedgerLocator, TransferLayout]:
    ledgers: LedgerLocator = LedgerLocator(tmp_path / "m")
    layout: TransferLayout = TransferLayout(tmp_path / "t")
    return ReceiptConfirmer(ledgers, layout, JsonModelStore()), ledgers, layout


STATE: RepositoryState = RepositoryState(default_branch="main", refs={"refs/heads/main": "c1"})


def test_confirm_promotes_the_received_state(
    confirmer_parts: tuple[ReceiptConfirmer, LedgerLocator, TransferLayout],
) -> None:
    confirmer, ledgers, layout = confirmer_parts
    JsonModelStore().save(ledgers.export_ledger("a"), ExportLedger().with_pending(STATE))
    JsonModelStore().save(
        layout.receipt_path,
        ImportReceipt(imported_at=MOMENT, entries=[ImportedState(name="a", state_id=STATE.state_id)]),
    )
    confirmer.confirm()
    ledger: ExportLedger | None = JsonModelStore().load(ledgers.export_ledger("a"), ExportLedger)
    assert (ledger.confirmed if ledger else None) == STATE


def test_confirm_ignores_a_state_it_never_sent(
    confirmer_parts: tuple[ReceiptConfirmer, LedgerLocator, TransferLayout],
) -> None:
    confirmer, _, layout = confirmer_parts
    JsonModelStore().save(
        layout.receipt_path, ImportReceipt(imported_at=MOMENT, entries=[ImportedState(name="a", state_id="x")])
    )
    assert confirmer.confirm() == 0


def test_confirm_twice_counts_once(confirmer_parts: tuple[ReceiptConfirmer, LedgerLocator, TransferLayout]) -> None:
    confirmer, ledgers, layout = confirmer_parts
    JsonModelStore().save(ledgers.export_ledger("a"), ExportLedger().with_pending(STATE))
    JsonModelStore().save(
        layout.receipt_path,
        ImportReceipt(imported_at=MOMENT, entries=[ImportedState(name="a", state_id=STATE.state_id)]),
    )
    confirmer.confirm()
    assert confirmer.confirm() == 0


def test_confirm_without_a_receipt_fails_clearly(
    confirmer_parts: tuple[ReceiptConfirmer, LedgerLocator, TransferLayout],
) -> None:
    assert ConfirmCommand(confirmer_parts[0]).run() == ["confirm"]
