from collections.abc import Callable, Iterator
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from airgap_mirrors.settings import ExternalRepoSpec, ExternalSettings, InternalRepoSpec, InternalSettings
from tests.support.fake_servers import FakeGitHub, FakeGitLab, FakeServer
from tests.support.upstream import UpstreamRepository

TOKEN: str = "glpat-test-token"


class SteppingClock:
    """Each call is one second later than the last, so transfers made in one test still sort in order."""

    def __init__(self) -> None:
        self._moment: datetime = datetime(2026, 1, 1, tzinfo=UTC)

    def now(self) -> datetime:
        self._moment += timedelta(seconds=1)
        return self._moment


@pytest.fixture
def clock() -> SteppingClock:
    return SteppingClock()


@pytest.fixture
def github_root(tmp_path: Path) -> Path:
    return tmp_path / "github"


@pytest.fixture
def make_upstream(github_root: Path) -> Callable[..., UpstreamRepository]:
    def make(owner: str = "acme", name: str = "widget", default_branch: str = "main") -> UpstreamRepository:
        return UpstreamRepository(github_root, owner, name, default_branch)

    return make


@pytest.fixture
def gitlab_server() -> Iterator[FakeGitLab]:
    with FakeServer() as server:
        yield FakeGitLab(server)


@pytest.fixture
def github_server() -> Iterator[FakeGitHub]:
    with FakeServer() as server:
        yield FakeGitHub(server)


@pytest.fixture
def gitlab_repositories(tmp_path: Path) -> Path:
    return tmp_path / "gitlab"


@pytest.fixture
def external_settings(tmp_path: Path, github_root: Path) -> Callable[..., ExternalSettings]:
    def build(repos: list[ExternalRepoSpec], github_api_url: str = "http://127.0.0.1:9") -> ExternalSettings:
        return ExternalSettings(
            mirrors_dir=tmp_path / "online-mirrors",
            transfer_dir=tmp_path / "transfer",
            github_url=github_root.as_uri(),
            github_api_url=github_api_url,
            http_timeout_seconds=10,
            repos=repos,
        )

    return build


@pytest.fixture
def internal_settings(
    tmp_path: Path, gitlab_server: FakeGitLab, gitlab_repositories: Path, monkeypatch: pytest.MonkeyPatch
) -> Callable[..., InternalSettings]:
    monkeypatch.setenv("GITLAB_TOKEN", TOKEN)

    def build(repos: list[InternalRepoSpec]) -> InternalSettings:
        return InternalSettings(
            mirrors_dir=tmp_path / "airgap-mirrors",
            transfer_dir=tmp_path / "transfer",
            gitlab_url=gitlab_server.server.url,
            git_remote_base=gitlab_repositories.as_uri(),
            release_package_name="release-assets",
            http_timeout_seconds=10,
            repos=repos,
        )

    return build
