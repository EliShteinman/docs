from pathlib import Path
from unittest.mock import MagicMock

import pytest
from pydantic import SecretStr
from pytest_mock import MockerFixture

from airgap_mirrors.exceptions import ConfigurationError
from airgap_mirrors.internal import GitLabClient, GitLabGroup, GitLabProject, HelmValuesWriter, ProjectProvisioner
from airgap_mirrors.settings import InternalRepoSpec, InternalSettings, ProjectVisibility
from airgap_mirrors.storage import JsonModelStore
from airgap_mirrors.transfer import TransferLayout

SPEC: InternalRepoSpec = InternalRepoSpec(name="redis", gitlab_path="top/mirrors/redis")
CREATED: GitLabProject = GitLabProject(id=7, path_with_namespace="top/mirrors/redis")


@pytest.fixture
def gitlab(mocker: MockerFixture) -> MagicMock:
    client: MagicMock = mocker.create_autospec(GitLabClient, instance=True)
    client.project.return_value = None
    client.group.side_effect = lambda path: GitLabGroup(id=1, full_path="top") if path == "top" else None
    client.create_group.return_value = GitLabGroup(id=2, full_path="top/mirrors")
    client.create_project.return_value = CREATED
    return client


def test_existing_project_is_used_as_it_is(gitlab: MagicMock) -> None:
    gitlab.project.return_value = CREATED
    ProjectProvisioner(gitlab, None).ensure_project(SPEC, "https://github.com/redis/redis")
    gitlab.create_project.assert_not_called()


def test_missing_subgroup_is_created_under_the_existing_parent(gitlab: MagicMock) -> None:
    ProjectProvisioner(gitlab, None).ensure_project(SPEC, "https://github.com/redis/redis")
    gitlab.create_group.assert_called_once_with("mirrors", 1, None)


def test_missing_project_is_created_in_its_group(gitlab: MagicMock) -> None:
    ProjectProvisioner(gitlab, ProjectVisibility.INTERNAL).ensure_project(SPEC, "https://github.com/redis/redis")
    gitlab.create_project.assert_called_once_with(
        2, "redis", "Copy of https://github.com/redis/redis, kept in sync from outside", "internal"
    )


def test_group_is_looked_up_once_for_several_projects(gitlab: MagicMock) -> None:
    provisioner: ProjectProvisioner = ProjectProvisioner(gitlab, None)
    provisioner.ensure_project(SPEC, "u")
    provisioner.ensure_project(InternalRepoSpec(name="jedis", gitlab_path="top/mirrors/jedis"), "u")
    gitlab.create_group.assert_called_once()


def test_missing_top_group_is_not_created(gitlab: MagicMock) -> None:
    gitlab.group.side_effect = lambda _path: None
    with pytest.raises(ConfigurationError, match="no group 'top'"):
        ProjectProvisioner(gitlab, None).ensure_project(SPEC, "u")


@pytest.fixture
def writer(tmp_path: Path) -> HelmValuesWriter:
    return HelmValuesWriter(tmp_path / "published.json", tmp_path / "values.yaml", JsonModelStore())


def test_helm_values_list_every_project(writer: HelmValuesWriter, tmp_path: Path) -> None:
    writer.record({"redis": "https://gl/m/redis"})
    assert (
        (tmp_path / "values.yaml")
        .read_text()
        .endswith('  gitMirrors:\n    "redis":\n      enabled: true\n      to: "https://gl/m/redis"\n')
    )


def test_helm_values_keep_projects_from_earlier_imports(writer: HelmValuesWriter, tmp_path: Path) -> None:
    writer.record({"redis": "https://gl/m/redis"})
    writer.record({"jedis": "https://gl/m/jedis"})
    assert '"redis":' in (tmp_path / "values.yaml").read_text()


@pytest.fixture
def settings(tmp_path: Path) -> InternalSettings:
    return InternalSettings(
        mirrors_dir=tmp_path,
        transfer_dir=tmp_path,
        gitlab_url="https://gl",
        gitlab_group="top/mirrors",
        release_package_name="p",
        http_timeout_seconds=5,
        GITLAB_TOKEN=SecretStr("x"),
        repos=[InternalRepoSpec(name="redis", gitlab_path="elsewhere/redis-server")],
    )


def test_repository_goes_into_the_group_by_default(settings: InternalSettings) -> None:
    assert settings.spec_for("jedis").gitlab_path == "top/mirrors/jedis"


def test_repository_block_overrides_the_path(settings: InternalSettings) -> None:
    assert settings.spec_for("redis").gitlab_path == "elsewhere/redis-server"


def test_transfer_folder_lists_its_repositories(tmp_path: Path) -> None:
    layout: TransferLayout = TransferLayout(tmp_path)
    layout.git_dir("redis").mkdir(parents=True)
    layout.asset_dir("RedisInsight", "3.10.0").mkdir(parents=True)
    assert layout.repository_names() == ["RedisInsight", "redis"]


def test_empty_transfer_folder_lists_nothing(tmp_path: Path) -> None:
    assert TransferLayout(tmp_path / "absent").repository_names() == []
