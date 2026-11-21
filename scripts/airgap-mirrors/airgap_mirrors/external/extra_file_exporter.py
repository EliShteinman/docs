import logging
from pathlib import Path

from airgap_mirrors.http import HttpClient
from airgap_mirrors.models import SentAssets
from airgap_mirrors.settings import ExternalRepoSpec, ExtraFile
from airgap_mirrors.storage import JsonModelStore, LedgerLocator
from airgap_mirrors.transfer import TransferLayout

logger: logging.Logger = logging.getLogger(__name__)


class ExtraFileExporter:
    """Online side. Downloads the files a repository needs but does not keep in git, each to its path inside the
    repository, under <transfer>/extra/<repo>/.

    A file sent by an earlier export is not sent again (export --full sends it anyway); changing its url in the
    config sends it again. The client sends no GitHub token: these files live on other servers."""

    def __init__(self, http: HttpClient, layout: TransferLayout, ledgers: LedgerLocator, store: JsonModelStore) -> None:
        self._http: HttpClient = http
        self._layout: TransferLayout = layout
        self._ledgers: LedgerLocator = ledgers
        self._store: JsonModelStore = store

    def export(self, spec: ExternalRepoSpec, *, full: bool = False) -> int:
        if not spec.extra_files:
            return 0
        ledger_path: Path = self._ledgers.sent_extra_files(spec.name)
        sent: SentAssets = SentAssets() if full else (self._store.load(ledger_path, SentAssets) or SentAssets())
        downloaded: int = 0
        for extra in spec.extra_files:
            if extra.ledger_key in sent.files:
                logger.debug("%s: %s was sent before", spec.name, extra.path)
                continue
            self._download(spec, extra)
            downloaded += 1
            sent = sent.with_file(extra.ledger_key)
            self._store.save(ledger_path, sent)
        logger.info("%s: %d new extra files", spec.name, downloaded)
        return downloaded

    def _download(self, spec: ExternalRepoSpec, extra: ExtraFile) -> None:
        logger.info("%s: downloading %s", spec.name, extra.path)
        self._http.download(extra.url, self._layout.extra_file(spec.name, extra.path))
