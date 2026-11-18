import logging

from airgap_mirrors.commands.repository_batch import RepositoryBatch
from airgap_mirrors.internal import GitImporter, HelmValuesWriter, ImportResult, ReleaseImporter
from airgap_mirrors.models import ImportedState, ImportReceipt
from airgap_mirrors.settings import InternalRepoSpec, InternalSettings, pick
from airgap_mirrors.storage import JsonModelStore
from airgap_mirrors.transfer import Clock, TransferLayout

logger: logging.Logger = logging.getLogger(__name__)


class ImportCommand:
    def __init__(
        self,
        settings: InternalSettings,
        git: GitImporter,
        releases: ReleaseImporter | None,
        helm_values: HelmValuesWriter,
        batch: RepositoryBatch,
        layout: TransferLayout,
        store: JsonModelStore,
        clock: Clock,
    ) -> None:
        self._settings: InternalSettings = settings
        self._git: GitImporter = git
        self._helm_values: HelmValuesWriter = helm_values
        self._releases: ReleaseImporter | None = releases
        self._batch: RepositoryBatch = batch
        self._layout: TransferLayout = layout
        self._store: JsonModelStore = store
        self._clock: Clock = clock

    def run(self, wanted: list[str]) -> list[str]:
        specs: list[InternalRepoSpec] = self._specs(wanted)
        imported: list[ImportedState] = []
        projects: dict[str, str] = {}

        def import_git(spec: InternalRepoSpec) -> None:
            result: ImportResult = self._git.import_repository(spec)
            imported.extend(ImportedState(name=spec.name, state_id=state_id) for state_id in result.state_ids)
            if result.project_url:
                projects[spec.name] = result.project_url

        failed: list[str] = self._batch.run("git import", specs, import_git)
        if self._releases is not None:
            releases: ReleaseImporter = self._releases
            failed += self._batch.run(
                "release import", [spec for spec in specs if spec.name not in failed], releases.import_repository
            )
        if projects:
            self._helm_values.record(projects)
        self._store.save(self._layout.receipt_path, ImportReceipt(imported_at=self._clock.now(), entries=imported))
        logger.info(
            "receipt written to %s: copy it back and run confirm on the online machine", self._layout.receipt_path
        )
        return failed

    def _specs(self, wanted: list[str]) -> list[InternalRepoSpec]:
        found: list[InternalRepoSpec] = [self._settings.spec_for(name) for name in self._layout.repository_names()]
        if not found:
            logger.warning("the transfer folder %s is empty: nothing to import", self._layout.root)
        logger.info("found in the transfer folder: %s", ", ".join(spec.name for spec in found) or "nothing")
        return pick(found, wanted)
