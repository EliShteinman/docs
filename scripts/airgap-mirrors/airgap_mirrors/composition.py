import ssl
from pathlib import Path

from airgap_mirrors.commands import ConfirmCommand, ExportCommand, ImportCommand, RepositoryBatch
from airgap_mirrors.exceptions import GitHubApiError, GitLabApiError
from airgap_mirrors.external import GitExporter, GitHubClient, ReceiptConfirmer, ReleaseExporter
from airgap_mirrors.git import BareRepository, GitRunner
from airgap_mirrors.http import HttpClient
from airgap_mirrors.internal import GitImporter, GitLabClient, ReleaseImporter, gitlab_git_config
from airgap_mirrors.settings import ExternalSettings, InternalSettings
from airgap_mirrors.storage import JsonModelStore, LedgerLocator
from airgap_mirrors.transfer import Clock, SystemClock, TransferLayout


class Composition:
    """Builds every object the commands need from the settings. The only place that knows the concrete classes."""

    def __init__(self, clock: Clock | None = None, store: JsonModelStore | None = None) -> None:
        self._clock: Clock = clock or SystemClock()
        self._store: JsonModelStore = store or JsonModelStore()

    def git_exporter(self, settings: ExternalSettings) -> GitExporter:
        git: GitRunner = GitRunner()
        return GitExporter(
            settings,
            lambda path: BareRepository(path, git),
            TransferLayout(settings.transfer_dir),
            LedgerLocator(settings.mirrors_dir),
            self._store,
            self._clock,
        )

    def export_command(self, settings: ExternalSettings, *, with_releases: bool) -> ExportCommand:
        releases: ReleaseExporter | None = None
        if with_releases:
            github: GitHubClient = GitHubClient(self._github_http(settings))
            releases = ReleaseExporter(github, TransferLayout(settings.transfer_dir), self._store)
        return ExportCommand(self.git_exporter(settings), releases, RepositoryBatch())

    def confirm_command(self, settings: ExternalSettings) -> ConfirmCommand:
        return ConfirmCommand(
            ReceiptConfirmer(LedgerLocator(settings.mirrors_dir), TransferLayout(settings.transfer_dir), self._store)
        )

    def git_importer(self, settings: InternalSettings) -> GitImporter:
        git: GitRunner = GitRunner(config=gitlab_git_config(settings))
        return GitImporter(
            settings,
            lambda path: BareRepository(path, git),
            TransferLayout(settings.transfer_dir),
            LedgerLocator(settings.mirrors_dir),
            self._store,
            GitLabClient(self._gitlab_http(settings)),
        )

    def import_command(self, settings: InternalSettings, *, with_releases: bool) -> ImportCommand:
        layout: TransferLayout = TransferLayout(settings.transfer_dir)
        releases: ReleaseImporter | None = None
        if with_releases:
            gitlab: GitLabClient = GitLabClient(self._gitlab_http(settings))
            releases = ReleaseImporter(gitlab, layout, self._store, settings.release_package_name)
        return ImportCommand(self.git_importer(settings), releases, RepositoryBatch(), layout, self._store, self._clock)

    @staticmethod
    def _github_http(settings: ExternalSettings) -> HttpClient:
        headers: dict[str, str] = {"Accept": "application/vnd.github+json"}
        if settings.github_token is not None:
            headers["Authorization"] = f"Bearer {settings.github_token.get_secret_value()}"
        return HttpClient(settings.github_api_url, headers, GitHubApiError, settings.http_timeout_seconds)

    @staticmethod
    def _gitlab_http(settings: InternalSettings) -> HttpClient:
        return HttpClient(
            f"{settings.gitlab_url.rstrip('/')}/api/v4",
            {"PRIVATE-TOKEN": settings.gitlab_token.get_secret_value()},
            GitLabApiError,
            settings.http_timeout_seconds,
            _ssl_context(settings.ca_file),
        )


def _ssl_context(ca_file: Path | None) -> ssl.SSLContext | None:
    return ssl.create_default_context(cafile=str(ca_file)) if ca_file else None
