import logging

from airgap_mirrors.commands.repository_batch import RepositoryBatch
from airgap_mirrors.internal import GitImporter, ReleaseImporter
from airgap_mirrors.models import ImportedState, ImportReceipt
from airgap_mirrors.settings import InternalRepoSpec
from airgap_mirrors.storage import JsonModelStore
from airgap_mirrors.transfer import Clock, TransferLayout

logger: logging.Logger = logging.getLogger(__name__)


class ImportCommand:
    def __init__(
        self,
        git: GitImporter,
        releases: ReleaseImporter | None,
        batch: RepositoryBatch,
        layout: TransferLayout,
        store: JsonModelStore,
        clock: Clock,
    ) -> None:
        self._git: GitImporter = git
        self._releases: ReleaseImporter | None = releases
        self._batch: RepositoryBatch = batch
        self._layout: TransferLayout = layout
        self._store: JsonModelStore = store
        self._clock: Clock = clock

    def run(self, specs: list[InternalRepoSpec]) -> list[str]:
        imported: list[ImportedState] = []

        def import_git(spec: InternalRepoSpec) -> None:
            imported.extend(
                ImportedState(name=spec.name, state_id=state_id) for state_id in self._git.import_repository(spec)
            )

        failed: list[str] = self._batch.run("git import", specs, import_git)
        if self._releases is not None:
            releases: ReleaseImporter = self._releases
            failed += self._batch.run(
                "release import", [spec for spec in specs if spec.name not in failed], releases.import_repository
            )
        self._store.save(self._layout.receipt_path, ImportReceipt(imported_at=self._clock.now(), entries=imported))
        logger.info(
            "receipt written to %s: copy it back and run confirm on the online machine", self._layout.receipt_path
        )
        return failed
