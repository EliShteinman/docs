import logging
from pathlib import Path

from airgap_mirrors.external.github_client import GitHubClient
from airgap_mirrors.models import ReleaseAsset, ReleaseCatalog, ReleaseRecord, SentAssets
from airgap_mirrors.settings import ExternalRepoSpec
from airgap_mirrors.storage import JsonModelStore, LedgerLocator
from airgap_mirrors.transfer import TransferLayout

logger: logging.Logger = logging.getLogger(__name__)


class ReleaseExporter:
    """Online side. Writes every release's notes, and the files of the releases the repository's policy picks.

    A file sent by an earlier export is not sent again (export --full sends it anyway). A file already in the
    transfer folder with the right size is not downloaded again, so an interrupted export picks up where it
    stopped."""

    def __init__(
        self, github: GitHubClient, layout: TransferLayout, ledgers: LedgerLocator, store: JsonModelStore
    ) -> None:
        self._github: GitHubClient = github
        self._layout: TransferLayout = layout
        self._ledgers: LedgerLocator = ledgers
        self._store: JsonModelStore = store

    def export(self, spec: ExternalRepoSpec, *, full: bool = False) -> int:
        releases: list[ReleaseRecord] = self._github.published_releases(spec.github)
        self._store.save(
            self._layout.releases_file(spec.name), ReleaseCatalog(repository=spec.github, releases=releases)
        )
        ledger_path: Path = self._ledgers.sent_assets(spec.name)
        sent: SentAssets = SentAssets() if full else (self._store.load(ledger_path, SentAssets) or SentAssets())
        downloaded: int = 0
        for release in spec.asset_policy.select(releases):
            for asset in release.assets:
                key: str = f"{release.tag_name}/{asset.name}"
                if not spec.wants_asset(asset.name) or key in sent.files:
                    continue
                downloaded += self._download(spec, release, asset)
                sent = sent.with_file(key)
                self._store.save(ledger_path, sent)
        logger.info("%s: %d releases, %d new files", spec.name, len(releases), downloaded)
        return downloaded

    def _download(self, spec: ExternalRepoSpec, release: ReleaseRecord, asset: ReleaseAsset) -> int:
        target: Path = self._layout.asset_dir(spec.name, release.tag_name) / asset.name
        if target.is_file() and target.stat().st_size == asset.size:
            logger.debug("%s: %s/%s already in the transfer folder", spec.name, release.tag_name, asset.name)
            return 0
        logger.info("%s: downloading %s/%s", spec.name, release.tag_name, asset.name)
        self._github.download(asset.download_url, target)
        return 1
