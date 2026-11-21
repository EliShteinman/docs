import logging

from airgap_mirrors.commands.repository_batch import RepositoryBatch
from airgap_mirrors.external import ExtraFileExporter, GitExporter, ReleaseExporter
from airgap_mirrors.settings import ExternalRepoSpec

logger: logging.Logger = logging.getLogger(__name__)


class ExportCommand:
    def __init__(
        self,
        git: GitExporter,
        releases: ReleaseExporter | None,
        extra_files: ExtraFileExporter,
        batch: RepositoryBatch,
    ) -> None:
        self._git: GitExporter = git
        self._releases: ReleaseExporter | None = releases
        self._extra_files: ExtraFileExporter = extra_files
        self._batch: RepositoryBatch = batch

    def run(self, specs: list[ExternalRepoSpec], *, full: bool) -> list[str]:
        failed: list[str] = self._batch.run("git export", specs, lambda spec: self._git.export(spec, full=full))
        if self._releases is not None:
            releases: ReleaseExporter = self._releases
            failed += self._batch.run("release export", specs, lambda spec: releases.export(spec, full=full))
        failed += self._batch.run("extra files export", specs, lambda spec: self._extra_files.export(spec, full=full))
        if not failed:
            logger.info("done: copy the transfer folder to the USB stick, then empty it; run import on the other side")
        return failed
