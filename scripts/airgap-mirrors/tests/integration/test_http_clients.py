from pathlib import Path

import pytest

from airgap_mirrors.exceptions import GitHubApiError, GitLabApiError
from airgap_mirrors.external import GitHubClient
from airgap_mirrors.http import HttpClient
from airgap_mirrors.internal import GitLabClient
from airgap_mirrors.models import ReleaseRecord
from tests.support.fake_servers import FakeGitHub, FakeGitLab, FakeProject, FakeServer

pytestmark = pytest.mark.integration

NESTED_PATH: str = "mirrors/redis/core/redis"


def github_client(server: FakeServer) -> GitHubClient:
    return GitHubClient(HttpClient(server.url, {"Authorization": "Bearer ghp-secret"}, GitHubApiError, 5))


def gitlab_client(server: FakeServer) -> GitLabClient:
    return GitLabClient(HttpClient(f"{server.url}/api/v4", {"PRIVATE-TOKEN": "glpat"}, GitLabApiError, 5))


def test_releases_are_read_across_pages(github_server: FakeGitHub) -> None:
    for number in range(5):
        github_server.add_release("acme/tool", f"v{number}", "2026-01-01T00:00:00Z", {})
    assert len(github_client(github_server.server).published_releases("acme/tool")) == 5


def test_draft_releases_are_left_out(github_server: FakeGitHub) -> None:
    github_server.add_release("acme/tool", "v1", "2026-01-01T00:00:00Z", {})
    github_server.add_release("acme/tool", "v2", "2026-01-02T00:00:00Z", {}, draft=True)
    releases: list[ReleaseRecord] = github_client(github_server.server).published_releases("acme/tool")
    assert [release.tag_name for release in releases] == ["v1"]


def test_release_file_is_downloaded(github_server: FakeGitHub, tmp_path: Path) -> None:
    github_server.add_release("acme/tool", "v1", "2026-01-01T00:00:00Z", {"tool.tgz": b"payload"})
    github_client(github_server.server).download(f"{github_server.server.url}/files/v1/tool.tgz", tmp_path / "tool.tgz")
    assert (tmp_path / "tool.tgz").read_bytes() == b"payload"


def test_token_is_not_forwarded_to_the_redirect_target(tmp_path: Path) -> None:
    with FakeServer() as server:
        server.route("GET", r"/asset", lambda **_: (302, b"", {"Location": f"{server.url}/storage"}))
        server.route("GET", r"/storage", lambda **_: (200, b"data", {}))
        github_client(server).download(f"{server.url}/asset", tmp_path / "file")
        assert "Authorization" not in server.requests[-1][2]


def test_failed_download_leaves_no_partial_file(github_server: FakeGitHub, tmp_path: Path) -> None:
    with pytest.raises(GitHubApiError):
        github_client(github_server.server).download(f"{github_server.server.url}/files/none", tmp_path / "f")
    assert list(tmp_path.iterdir()) == []


def test_unreachable_server_is_an_api_error(tmp_path: Path) -> None:
    client: HttpClient = HttpClient("http://127.0.0.1:9", {}, GitLabApiError, 2)
    with pytest.raises(GitLabApiError):
        client.get("anything")


@pytest.fixture
def project(gitlab_server: FakeGitLab, tmp_path: Path) -> FakeProject:
    return gitlab_server.add_project(NESTED_PATH, tmp_path / "project.git")


def test_project_is_found_by_its_nested_path(gitlab_server: FakeGitLab, project: FakeProject) -> None:
    found = gitlab_client(gitlab_server.server).project(NESTED_PATH)
    assert (found.id if found else None) == project.id


def test_unknown_project_is_none(gitlab_server: FakeGitLab) -> None:
    assert gitlab_client(gitlab_server.server).project("no/such") is None


def test_server_error_is_raised_not_hidden(tmp_path: Path) -> None:
    with FakeServer() as server:
        server.route("GET", r"/api/v4/projects/([^/]+)", lambda *_, **__: (500, {"message": "boom"}, {}))
        with pytest.raises(GitLabApiError, match="500"):
            gitlab_client(server).project("g/p")


def test_default_branch_is_set(gitlab_server: FakeGitLab, project: FakeProject) -> None:
    gitlab_client(gitlab_server.server).set_default_branch(NESTED_PATH, "unstable")
    assert project.default_branch == "unstable"


def test_release_link_gets_a_permanent_download_path(gitlab_server: FakeGitLab, project: FakeProject) -> None:
    gitlab_client(gitlab_server.server).link_release_file(NESTED_PATH, "v1", "tool.tgz", "https://x")
    assert project.links["v1"][0]["direct_asset_path"] == "/tool.tgz"


def test_package_upload_returns_the_download_url(
    gitlab_server: FakeGitLab, project: FakeProject, tmp_path: Path
) -> None:
    (tmp_path / "tool.tgz").write_bytes(b"payload")
    url: str = gitlab_client(gitlab_server.server).upload_package_file(NESTED_PATH, "pkg", "v1", tmp_path / "tool.tgz")
    assert url.endswith("/projects/mirrors%2Fredis%2Fcore%2Fredis/packages/generic/pkg/v1/tool.tgz")


def test_package_upload_sends_the_file(gitlab_server: FakeGitLab, project: FakeProject, tmp_path: Path) -> None:
    (tmp_path / "tool.tgz").write_bytes(b"payload")
    gitlab_client(gitlab_server.server).upload_package_file(NESTED_PATH, "pkg", "v1", tmp_path / "tool.tgz")
    assert project.packages["pkg/v1/tool.tgz"] == b"payload"
