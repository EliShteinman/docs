import hashlib
import logging
from pathlib import Path

from airgap_mirrors.internal.gitlab_client import GitLabClient
from airgap_mirrors.models import UploadedExtraFiles
from airgap_mirrors.settings import InternalRepoSpec
from airgap_mirrors.storage import JsonModelStore, LedgerLocator
from airgap_mirrors.transfer import TransferLayout

logger: logging.Logger = logging.getLogger(__name__)


class ExtraFileImporter:
    """Air-gapped side. Uploads each extra file to the project's generic package registry, at
    <project>/packages/generic/<package>/<version>/<file name>, a fixed address a build can download from.

    Safe to run again: a file whose content was already uploaded is skipped."""

    def __init__(
        self,
        gitlab: GitLabClient,
        layout: TransferLayout,
        ledgers: LedgerLocator,
        store: JsonModelStore,
        package_name: str,
        package_version: str,
    ) -> None:
        self._gitlab: GitLabClient = gitlab
        self._layout: TransferLayout = layout
        self._ledgers: LedgerLocator = ledgers
        self._store: JsonModelStore = store
        self._package_name: str = package_name
        self._package_version: str = package_version

    def import_repository(self, spec: InternalRepoSpec) -> int:
        directory: Path = self._layout.extra_dir(spec.name)
        if not directory.is_dir():
            return 0
        ledger_path: Path = self._ledgers.uploaded_extra_files(spec.name)
        uploaded: UploadedExtraFiles = self._store.load(ledger_path, UploadedExtraFiles) or UploadedExtraFiles()
        count: int = 0
        for file in _files_under(directory):
            path: str = file.relative_to(directory).as_posix()
            digest: str = _sha256(file)
            if uploaded.digests.get(path) == digest:
                logger.debug("%s: %s already uploaded", spec.name, path)
                continue
            url: str = self._gitlab.upload_package_file(
                spec.gitlab_path, self._package_name, self._package_version, file
            )
            logger.info("%s: %s -> %s", spec.name, path, url)
            uploaded = uploaded.with_upload(path, digest)
            self._store.save(ledger_path, uploaded)
            count += 1
        logger.info("%s: extra files done, %d uploaded", spec.name, count)
        return count


def _files_under(directory: Path) -> list[Path]:
    return sorted(path for path in directory.rglob("*") if path.is_file() and not path.name.startswith("."))


def _sha256(file: Path) -> str:
    with file.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()
