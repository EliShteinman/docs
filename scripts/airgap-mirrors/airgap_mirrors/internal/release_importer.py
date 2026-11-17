import logging
import re
from pathlib import Path

from airgap_mirrors.internal.gitlab_client import GitLabClient
from airgap_mirrors.models import ReleaseCatalog, ReleaseRecord
from airgap_mirrors.settings import InternalRepoSpec
from airgap_mirrors.storage import JsonModelStore
from airgap_mirrors.transfer import TransferLayout

logger: logging.Logger = logging.getLogger(__name__)

_UNSAFE_VERSION_CHARACTERS = re.compile(r"[^A-Za-z0-9._+-]")


class ReleaseImporter:
    """Air-gapped side. Creates each missing GitLab release, then uploads each file it does not have yet.

    Files go to the project's generic package registry; each release link gets a permanent address,
    <project>/-/releases/<tag>/downloads/<file>, which is where the docs' download links are sent.
    Safe to run again: a release or file already there is skipped, and a file that failed is retried."""

    def __init__(self, gitlab: GitLabClient, layout: TransferLayout, store: JsonModelStore, package_name: str) -> None:
        self._gitlab: GitLabClient = gitlab
        self._layout: TransferLayout = layout
        self._store: JsonModelStore = store
        self._package_name: str = package_name

    def import_repository(self, spec: InternalRepoSpec) -> int:
        catalog: ReleaseCatalog | None = self._store.load(self._layout.releases_file(spec.name), ReleaseCatalog)
        if catalog is None:
            logger.info("%s: no releases in the transfer folder", spec.name)
            return 0
        uploaded: int = 0
        for release in catalog.releases:
            if not self._gitlab.tag_exists(spec.gitlab_path, release.tag_name):
                logger.warning(
                    "%s: tag %s is not in GitLab; import the git transfer first", spec.name, release.tag_name
                )
                continue
            if not self._gitlab.release_exists(spec.gitlab_path, release.tag_name):
                self._gitlab.create_release(spec.gitlab_path, release)
                logger.info("%s: created release %s", spec.name, release.tag_name)
            uploaded += self._upload_files(spec, release)
        logger.info("%s: releases done, %d files uploaded", spec.name, uploaded)
        return uploaded

    def _upload_files(self, spec: InternalRepoSpec, release: ReleaseRecord) -> int:
        directory: Path = self._layout.asset_dir(spec.name, release.tag_name)
        if not directory.is_dir():
            return 0
        linked: set[str] = self._gitlab.release_link_names(spec.gitlab_path, release.tag_name)
        uploaded: int = 0
        for file in sorted(path for path in directory.iterdir() if path.is_file() and not path.name.startswith(".")):
            if file.name in linked:
                continue
            url: str = self._gitlab.upload_package_file(
                spec.gitlab_path, self._package_name, package_version(release.tag_name), file
            )
            self._gitlab.link_release_file(spec.gitlab_path, release.tag_name, file.name, url)
            logger.info("%s: %s <- %s", spec.name, release.tag_name, file.name)
            uploaded += 1
        return uploaded


def package_version(tag: str) -> str:
    return _UNSAFE_VERSION_CHARACTERS.sub("-", tag)
