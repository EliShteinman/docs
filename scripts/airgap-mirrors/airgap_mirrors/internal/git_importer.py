import logging
from collections.abc import Callable
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from airgap_mirrors.exceptions import GitCommandError, MissingObjectsError, TransferError
from airgap_mirrors.git import BareRepository
from airgap_mirrors.git.bare_repository import BRANCHES_AND_TAGS
from airgap_mirrors.internal.gitlab_client import GitLabClient, GitLabProject
from airgap_mirrors.internal.project_provisioner import ProjectProvisioner
from airgap_mirrors.models import ImportLedger, RepositoryState, TransferManifest
from airgap_mirrors.settings import InternalRepoSpec, InternalSettings
from airgap_mirrors.storage import JsonModelStore, LedgerLocator
from airgap_mirrors.transfer import TransferLayout

logger: logging.Logger = logging.getLogger(__name__)


class ImportResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    state_ids: list[str] = Field(default_factory=list)
    project_url: str | None = None


class GitImporter:
    """Air-gapped side. Applies every transfer for a repository in order, then makes GitLab match the result.

    The order of the push is what keeps the default branch right:
      1. push the upstream default branch on its own,
      2. tell GitLab that branch is the default,
      3. push every other branch and tag, deleting the ones upstream deleted.
    GitLab never gets to pick a default of its own. When upstream renamed its default branch, GitLab still
    protects the old one, so that protection is removed between steps 2 and 3, letting step 3 delete it.
    """

    def __init__(
        self,
        settings: InternalSettings,
        repository_factory: Callable[[Path], BareRepository],
        layout: TransferLayout,
        ledgers: LedgerLocator,
        store: JsonModelStore,
        gitlab: GitLabClient,
        provisioner: ProjectProvisioner,
    ) -> None:
        self._settings: InternalSettings = settings
        self._repository_factory: Callable[[Path], BareRepository] = repository_factory
        self._layout: TransferLayout = layout
        self._ledgers: LedgerLocator = ledgers
        self._store: JsonModelStore = store
        self._gitlab: GitLabClient = gitlab
        self._provisioner: ProjectProvisioner = provisioner

    def import_repository(self, spec: InternalRepoSpec) -> ImportResult:
        manifests: list[TransferManifest] = self._manifests(spec)
        if not manifests:
            logger.info("%s: no git transfer in the folder", spec.name)
            return ImportResult()
        project: GitLabProject = self._provisioner.ensure_project(spec, manifests[-1].upstream_url)
        repository: BareRepository = self._local_copy(spec, project)
        for manifest in manifests:
            self._apply(spec, repository, manifest)
        final: RepositoryState = manifests[-1].state
        self._publish(spec, repository, project, final)
        return ImportResult(
            state_ids=[manifest.state.state_id for manifest in manifests],
            project_url=project.web_url or f"{self._settings.gitlab_url.rstrip('/')}/{spec.gitlab_path}",
        )

    def _manifests(self, spec: InternalRepoSpec) -> list[TransferManifest]:
        loaded: list[TransferManifest] = []
        for path in self._layout.manifest_paths(spec.name):
            manifest: TransferManifest | None = self._store.load(path, TransferManifest)
            if manifest is not None:
                loaded.append(manifest)
        return sorted(loaded, key=lambda manifest: manifest.created_at)

    def _local_copy(self, spec: InternalRepoSpec, project: GitLabProject) -> BareRepository:
        """A machine without a local copy starts from the commits GitLab already holds, so a transfer that builds
        on earlier ones still applies on a fresh machine. Only the newest commits come, not the whole history."""
        repository: BareRepository = self._repository_factory(self._ledgers.repository_path(spec.name))
        if repository.exists():
            return repository
        repository.create()
        if project.default_branch is not None:
            logger.info("%s: no local copy here; taking the latest commits GitLab holds, without files", spec.name)
            repository.seed_tips_from(self._settings.push_url(spec))
        return repository

    def _apply(self, spec: InternalRepoSpec, repository: BareRepository, manifest: TransferManifest) -> None:
        ledger_path: Path = self._ledgers.import_ledger(spec.name)
        ledger: ImportLedger = self._store.load(ledger_path, ImportLedger) or ImportLedger()
        if manifest.state.state_id in ledger.applied_state_ids:
            logger.debug("%s: transfer from %s already applied", spec.name, manifest.created_at)
            return
        if manifest.bundle_file:
            self._unpack(spec, repository, self._layout.git_dir(spec.name) / manifest.bundle_file)
        missing: set[str] = repository.missing_objects(manifest.state.object_ids())
        if missing:
            raise MissingObjectsError(spec.name, len(missing))
        repository.set_branches_and_tags(manifest.state.refs)
        repository.point_head_at(manifest.state.default_branch)
        self._store.save(ledger_path, ledger.with_applied(manifest.state.state_id))
        logger.info("%s: applied transfer from %s", spec.name, manifest.created_at.isoformat())

    def _release_old_default(self, spec: InternalRepoSpec, old_default: str | None, state: RepositoryState) -> None:
        if old_default is None or f"refs/heads/{old_default}" in state.refs:
            return
        if self._gitlab.unprotect_branch(spec.gitlab_path, old_default):
            logger.warning(
                "%s: %s is gone upstream; removed its GitLab protection so it can be deleted", spec.name, old_default
            )

    def _unpack(self, spec: InternalRepoSpec, repository: BareRepository, bundle: Path) -> None:
        try:
            repository.verify_bundle(bundle)
        except GitCommandError as unusable:
            raise TransferError(
                f"{spec.name}: {bundle.name} cannot be applied. Either the file was damaged on the way, or it builds "
                "on an earlier transfer that never arrived: bring that one over, or run export with --full."
            ) from unusable
        repository.unpack_bundle(bundle)

    def _publish(
        self, spec: InternalRepoSpec, repository: BareRepository, project: GitLabProject, state: RepositoryState
    ) -> None:
        url: str = self._settings.push_url(spec)
        default: str = state.default_branch
        repository.push(url, [f"+refs/heads/{default}:refs/heads/{default}"])
        if project.default_branch != default:
            logger.info("%s: default branch %s -> %s", spec.name, project.default_branch, default)
            self._gitlab.set_default_branch(spec.gitlab_path, default)
            self._release_old_default(spec, project.default_branch, state)
        repository.push(url, BRANCHES_AND_TAGS, prune=True)
        logger.info("%s: GitLab is up to date (%d branches and tags)", spec.name, len(state.refs))
