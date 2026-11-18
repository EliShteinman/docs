from collections.abc import Callable
from pathlib import Path

import pytest

from airgap_mirrors.cli import EXIT_BAD_CONFIG, EXIT_OK, EXIT_SOME_FAILED, main
from airgap_mirrors.composition import Composition
from tests.conftest import TOKEN, SteppingClock
from tests.support.fake_servers import FakeGitHub, FakeGitLab, FakeProject
from tests.support.upstream import UpstreamRepository, git

pytestmark = pytest.mark.e2e

GITLAB_PATH: str = "mirrors/redis"
LOGGING: Path = Path(__file__).resolve().parents[2] / "config" / "logging.toml"


class Machines:
    """The two config files a real deployment has, and the command line run against each."""

    def __init__(self, online_config: Path, airgap_config: Path, clock: SteppingClock) -> None:
        self.online_config: Path = online_config
        self.airgap_config: Path = airgap_config
        self._clock: SteppingClock = clock

    def run(self, config: Path, *arguments: str) -> int:
        return main(
            ["--config", str(config), "--logging-config", str(LOGGING), *arguments], Composition(clock=self._clock)
        )

    def export(self, *arguments: str) -> int:
        return self.run(self.online_config, "export", *arguments)

    def import_(self, *arguments: str) -> int:
        return self.run(self.airgap_config, "import", *arguments)


@pytest.fixture
def upstream(make_upstream: Callable[..., UpstreamRepository]) -> UpstreamRepository:
    repository: UpstreamRepository = make_upstream(owner="redis", name="redis", default_branch="unstable")
    repository.tag("7.4.0")
    repository.commit("unstable", "server.c", "int main(void) {}")
    repository.tag("8.0.0")
    repository.pull_request_ref(42, repository.refs()["refs/heads/unstable"])
    return repository


@pytest.fixture
def machines(
    tmp_path: Path,
    github_root: Path,
    gitlab_repositories: Path,
    gitlab_server: FakeGitLab,
    github_server: FakeGitHub,
    upstream: UpstreamRepository,
    clock: SteppingClock,
    monkeypatch: pytest.MonkeyPatch,
) -> Machines:
    monkeypatch.setenv("GITLAB_TOKEN", TOKEN)
    gitlab_server.add_group("mirrors")
    github_server.add_release("redis/redis", "7.4.0", "2025-01-01T00:00:00Z", {"redis-7.4.0.tar.gz": b"old"})
    github_server.add_release(
        "redis/redis",
        "8.0.0",
        "2026-01-01T00:00:00Z",
        {"redis-8.0.0.tar.gz": b"tarball", "redis-8.0.0-mac.dmg": b"m", "redis-8.0.0-linux-arm64.tar.gz": b"a"},
    )
    online: Path = tmp_path / "external.toml"
    online.write_text(
        f'mirrors_dir = "{tmp_path / "online"}"\n'
        f'transfer_dir = "{tmp_path / "usb"}"\n'
        f'github_url = "{github_root.as_uri()}"\n'
        f'github_api_url = "{github_server.server.url}"\n'
        "http_timeout_seconds = 10\n"
        "download_attempts = 2\n"
        'default_assets = "latest-per-type"\n'
        'default_platforms = ["windows", "linux", "redhat"]\n'
        'default_architectures = ["x86_64"]\n\n'
        '[[repos]]\nname = "redis"\ngithub = "redis/redis"\n'
    )
    airgap: Path = tmp_path / "internal.toml"
    airgap.write_text(
        f'mirrors_dir = "{tmp_path / "airgap"}"\n'
        f'transfer_dir = "{tmp_path / "usb"}"\n'
        f'gitlab_url = "{gitlab_server.server.url}"\n'
        f'git_remote_base = "{gitlab_repositories.as_uri()}"\n'
        'release_package_name = "release-assets"\n'
        'gitlab_group = "mirrors"\n'
        "http_timeout_seconds = 10\n"
    )
    return Machines(online, airgap, clock)


@pytest.fixture
def transferred(machines: Machines) -> Machines:
    assert machines.export() == EXIT_OK
    assert machines.import_() == EXIT_OK
    return machines


@pytest.fixture
def project(transferred: Machines, gitlab_server: FakeGitLab) -> FakeProject:
    return gitlab_server.projects[GITLAB_PATH]


def gitlab_refs(project: FakeProject) -> set[str]:
    return set(git("for-each-ref", "--format=%(refname)", cwd=project.repository).splitlines())


def test_gitlab_gets_branches_and_tags(transferred: Machines, project: FakeProject) -> None:
    assert gitlab_refs(project) == {"refs/heads/unstable", "refs/tags/7.4.0", "refs/tags/8.0.0"}


def test_gitlab_default_branch_is_upstream_default(transferred: Machines, project: FakeProject) -> None:
    assert project.default_branch == "unstable"


def test_gitlab_gets_the_release_notes(transferred: Machines, project: FakeProject) -> None:
    assert project.releases["8.0.0"]["description"] == "notes for 8.0.0"


def test_gitlab_gets_the_release_file(transferred: Machines, project: FakeProject) -> None:
    assert project.packages["release-assets/8.0.0/redis-8.0.0.tar.gz"] == b"tarball"


def test_release_file_link_has_the_docs_download_path(transferred: Machines, project: FakeProject) -> None:
    assert project.links["8.0.0"][0]["direct_asset_path"] == "/redis-8.0.0.tar.gz"


def test_older_release_files_stay_behind(transferred: Machines, project: FakeProject) -> None:
    assert "release-assets/7.4.0/redis-7.4.0.tar.gz" not in project.packages


def test_files_for_unwanted_platforms_stay_behind(transferred: Machines, project: FakeProject) -> None:
    assert "release-assets/8.0.0/redis-8.0.0-mac.dmg" not in project.packages


def test_files_for_unwanted_architectures_stay_behind(transferred: Machines, project: FakeProject) -> None:
    assert "release-assets/8.0.0/redis-8.0.0-linux-arm64.tar.gz" not in project.packages


def test_older_release_notes_still_come(transferred: Machines, project: FakeProject) -> None:
    assert "7.4.0" in project.releases


def test_import_run_twice_changes_nothing(transferred: Machines, project: FakeProject) -> None:
    assert (transferred.import_(), len(project.links["8.0.0"])) == (EXIT_OK, 1)


def test_bad_config_exits_with_config_error(machines: Machines, tmp_path: Path) -> None:
    (tmp_path / "broken.toml").write_text("mirrors_dir = 1\n")
    assert machines.run(tmp_path / "broken.toml", "export") == EXIT_BAD_CONFIG


def test_unknown_repository_name_exits_with_config_error(machines: Machines) -> None:
    assert machines.export("--repo", "nope") == EXIT_BAD_CONFIG


def test_missing_gitlab_group_exits_with_failure(machines: Machines, gitlab_server: FakeGitLab) -> None:
    gitlab_server.groups.clear()
    machines.export("--skip-releases")
    assert machines.import_("--skip-releases") == EXIT_SOME_FAILED


def test_helm_values_point_each_repository_at_its_project(transferred: Machines, tmp_path: Path) -> None:
    values: str = (tmp_path / "airgap" / "helm-values-git-mirrors.yaml").read_text()
    assert '    "redis":\n      enabled: true\n      to: "https://gitlab.test/mirrors/redis"' in values


def test_import_of_a_repository_not_in_the_folder_exits_with_config_error(transferred: Machines) -> None:
    assert transferred.import_("--repo", "nope") == EXIT_BAD_CONFIG


def test_second_export_sends_no_release_file_twice(transferred: Machines, tmp_path: Path) -> None:
    for leftover in sorted((tmp_path / "usb").rglob("*"), reverse=True):
        leftover.unlink() if leftover.is_file() else leftover.rmdir()
    transferred.export()
    assert not list((tmp_path / "usb").rglob("*.tar.gz"))
