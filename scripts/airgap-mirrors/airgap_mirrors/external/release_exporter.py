import logging
from pathlib import Path

from airgap_mirrors.external.github_client import GitHubClient
from airgap_mirrors.models import ReleaseAsset, ReleaseCatalog, ReleaseRecord
from airgap_mirrors.settings import ExternalRepoSpec
from airgap_mirrors.storage import JsonModelStore
from airgap_mirrors.transfer import TransferLayout

logger: logging.Logger = logging.getLogger(__name__)


class ReleaseExporter:
    """Online side. Copies every release's notes, and the files of the releases the repository's policy picks.

    A file already in the transfer folder with the right size is not downloaded again."""

    def __init__(self, github: GitHubClient, layout: TransferLayout, store: JsonModelStore) -> None:
        self._github: GitHubClient = github
        self._layout: TransferLayout = layout
        self._store: JsonModelStore = store

    def export(self, spec: ExternalRepoSpec) -> int:
        releases: list[ReleaseRecord] = self._github.published_releases(spec.github)
        self._store.save(
            self._layout.releases_file(spec.name), ReleaseCatalog(repository=spec.github, releases=releases)
        )
        downloaded: int = sum(self._download_files(spec, release) for release in spec.assets.select(releases))
        logger.info("%s: %d releases, %d files downloaded", spec.name, len(releases), downloaded)
        return downloaded

    def _download_files(self, spec: ExternalRepoSpec, release: ReleaseRecord) -> int:
        downloaded: int = 0
        for asset in release.assets:
            if not spec.wants_asset(asset.name):
                continue
            target: Path = self._layout.asset_dir(spec.name, release.tag_name) / asset.name
            if _already_there(target, asset):
                logger.debug("%s: %s/%s already downloaded", spec.name, release.tag_name, asset.name)
                continue
            logger.info("%s: downloading %s/%s", spec.name, release.tag_name, asset.name)
            self._github.download(asset.download_url, target)
            downloaded += 1
        return downloaded


def _already_there(target: Path, asset: ReleaseAsset) -> bool:
    return target.is_file() and target.stat().st_size == asset.size
