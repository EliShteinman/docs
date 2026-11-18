import logging
from collections.abc import Callable
from datetime import datetime
from enum import StrEnum
from pathlib import Path

from airgap_mirrors.git import BareRepository
from airgap_mirrors.models import ExportLedger, RepositoryState, TransferManifest
from airgap_mirrors.settings import ExternalRepoSpec, ExternalSettings
from airgap_mirrors.storage import JsonModelStore, LedgerLocator
from airgap_mirrors.transfer import Clock, TransferLayout

logger: logging.Logger = logging.getLogger(__name__)


class ExportOutcome(StrEnum):
    UNCHANGED = "unchanged"
    REFS_ONLY = "refs only"
    BUNDLED = "bundled"


class GitExporter:
    """Online side. Brings the local copy up to date with GitHub and writes what GitLab is missing.

    "What GitLab is missing" is measured from the newest state still waiting in the transfer folder, or else
    from the last *confirmed* state: the one an import reported back. Emptying the folder without a confirm
    makes the next export repeat everything since that confirmed state, so a lost USB stick costs nothing.
    """

    def __init__(
        self,
        settings: ExternalSettings,
        repository_factory: Callable[[Path], BareRepository],
        layout: TransferLayout,
        ledgers: LedgerLocator,
        store: JsonModelStore,
        clock: Clock,
    ) -> None:
        self._settings: ExternalSettings = settings
        self._repository_factory: Callable[[Path], BareRepository] = repository_factory
        self._layout: TransferLayout = layout
        self._ledgers: LedgerLocator = ledgers
        self._store: JsonModelStore = store
        self._clock: Clock = clock

    def export(self, spec: ExternalRepoSpec, *, full: bool = False) -> ExportOutcome:
        repository: BareRepository = self._updated_repository(spec)
        state: RepositoryState = RepositoryState(
            default_branch=repository.upstream_default_branch(),
            refs=repository.branch_and_tag_tips(),
        )
        repository.point_head_at(state.default_branch)
        ledger_path: Path = self._ledgers.export_ledger(spec.name)
        ledger: ExportLedger = self._store.load(ledger_path, ExportLedger) or ExportLedger()
        waiting: RepositoryState | None = None if full else self._newest_waiting_in_folder(spec, ledger)
        if waiting is not None and waiting.state_id == state.state_id:
            logger.info("%s: this exact state is already in the transfer folder", spec.name)
            return ExportOutcome.UNCHANGED
        base: RepositoryState | None = None if full else (waiting or ledger.confirmed)
        if base is not None and base.state_id == state.state_id:
            logger.info("%s: nothing new since the last confirmed transfer", spec.name)
            return ExportOutcome.UNCHANGED
        outcome: ExportOutcome = self._write_transfer(spec, repository, state, base)
        self._store.save(ledger_path, ledger.with_pending(state))
        return outcome

    def _newest_waiting_in_folder(self, spec: ExternalRepoSpec, ledger: ExportLedger) -> RepositoryState | None:
        """The newest not-yet-confirmed state whose files are still in the transfer folder. Import applies the
        folder's transfers in order, so a new transfer can carry only what came after it."""
        newest: TransferManifest | None = None
        for path in self._layout.manifest_paths(spec.name):
            manifest: TransferManifest | None = self._store.load(path, TransferManifest)
            if manifest is None or manifest.state.state_id not in ledger.pending:
                continue
            if manifest.bundle_file is not None and not (path.parent / manifest.bundle_file).is_file():
                continue
            if newest is None or manifest.created_at > newest.created_at:
                newest = manifest
        return newest.state if newest else None

    def _updated_repository(self, spec: ExternalRepoSpec) -> BareRepository:
        repository: BareRepository = self._repository_factory(self._ledgers.repository_path(spec.name))
        if not repository.exists():
            repository.create()
        repository.track_upstream(self._settings.upstream_url(spec))
        repository.drop_refs_outside_branches_and_tags()
        logger.info("%s: fetching from %s", spec.name, spec.github)
        repository.fetch_upstream()
        return repository

    def _write_transfer(
        self,
        spec: ExternalRepoSpec,
        repository: BareRepository,
        state: RepositoryState,
        base: RepositoryState | None,
    ) -> ExportOutcome:
        created_at: datetime = self._clock.now()
        changed: list[str] = state.refs_changed_since(base)
        known: list[str] = sorted(
            object_id for object_id in (base.object_ids() if base else set()) if repository.has_object(object_id)
        )
        bundle_path: Path | None = None
        if changed and (base is None or repository.has_objects_beyond(changed, known)):
            bundle_path = self._layout.bundle_path(spec.name, created_at)
            repository.create_bundle(bundle_path, changed, known)
        manifest: TransferManifest = TransferManifest(
            name=spec.name,
            upstream_url=self._settings.upstream_url(spec),
            state=state,
            base_state_id=base.state_id if base else None,
            bundle_file=bundle_path.name if bundle_path else None,
            created_at=created_at,
        )
        self._store.save(self._layout.manifest_path(spec.name, created_at), manifest)
        return self._report(spec, state, base, bundle_path)

    def _report(
        self, spec: ExternalRepoSpec, state: RepositoryState, base: RepositoryState | None, bundle_path: Path | None
    ) -> ExportOutcome:
        kind: str = "full copy" if base is None else "changes"
        if bundle_path is None:
            logger.info("%s: %s with no new commits (default branch %s)", spec.name, kind, state.default_branch)
            return ExportOutcome.REFS_ONLY
        size_mib: float = bundle_path.stat().st_size / (1024 * 1024)
        logger.info("%s: %s, %.1f MiB (default branch %s)", spec.name, kind, size_mib, state.default_branch)
        return ExportOutcome.BUNDLED
