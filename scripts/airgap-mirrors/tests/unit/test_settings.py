from pathlib import Path

import pytest

from airgap_mirrors.exceptions import ConfigurationError
from airgap_mirrors.settings import (
    ExternalRepoSpec,
    ExternalSettings,
    InternalRepoSpec,
    InternalSettings,
    SettingsLoader,
    pick,
)

EXTERNAL_TOML: str = """
mirrors_dir = "/m"
transfer_dir = "/t"
github_url = "https://github.com"
github_api_url = "https://api.github.com"
http_timeout_seconds = 30

[[repos]]
name = "redis"
github = "redis/redis"
"""

INTERNAL_TOML: str = """
mirrors_dir = "/m"
transfer_dir = "/t"
gitlab_url = "https://gitlab.example"
release_package_name = "release-assets"
http_timeout_seconds = 30

[[repos]]
name = "redis"
gitlab_path = "group/sub/redis"
"""


@pytest.fixture
def write_config(tmp_path: Path):
    def write(text: str) -> Path:
        path: Path = tmp_path / "config.toml"
        path.write_text(text)
        return path

    return write


def test_external_config_loads(write_config) -> None:
    settings: ExternalSettings = SettingsLoader().load(write_config(EXTERNAL_TOML), ExternalSettings)
    assert settings.upstream_url(settings.repos[0]) == "https://github.com/redis/redis"


def test_github_token_comes_from_the_environment(write_config, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GITHUB_TOKEN", "ghp-secret")
    settings: ExternalSettings = SettingsLoader().load(write_config(EXTERNAL_TOML), ExternalSettings)
    assert (settings.github_token.get_secret_value() if settings.github_token else None) == "ghp-secret"


def test_internal_config_needs_the_gitlab_token(write_config, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GITLAB_TOKEN", raising=False)
    with pytest.raises(ConfigurationError, match="GITLAB_TOKEN"):
        SettingsLoader().load(write_config(INTERNAL_TOML), InternalSettings)


def test_push_url_defaults_to_the_gitlab_address(write_config, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GITLAB_TOKEN", "t")
    settings: InternalSettings = SettingsLoader().load(write_config(INTERNAL_TOML), InternalSettings)
    assert settings.push_url(settings.repos[0]) == "https://gitlab.example/group/sub/redis.git"


def test_push_url_uses_the_ssh_base_when_set(write_config, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GITLAB_TOKEN", "t")
    text: str = INTERNAL_TOML.replace("[[repos]]", 'git_remote_base = "ssh://git@gitlab.example"\n\n[[repos]]', 1)
    settings: InternalSettings = SettingsLoader().load(write_config(text), InternalSettings)
    assert settings.push_url(settings.repos[0]) == "ssh://git@gitlab.example/group/sub/redis.git"


def test_missing_config_file_is_reported(tmp_path: Path) -> None:
    with pytest.raises(ConfigurationError, match="not found"):
        SettingsLoader().load(tmp_path / "absent.toml", ExternalSettings)


def test_broken_toml_is_reported(write_config) -> None:
    with pytest.raises(ConfigurationError, match="not valid TOML"):
        SettingsLoader().load(write_config("mirrors_dir = "), ExternalSettings)


def test_unknown_key_is_refused(write_config) -> None:
    with pytest.raises(ConfigurationError, match="mirror_dir"):
        SettingsLoader().load(write_config(EXTERNAL_TOML + '\nmirror_dir = "/typo"\n'), ExternalSettings)


def test_repository_listed_twice_is_refused(write_config) -> None:
    doubled: str = EXTERNAL_TOML + '\n[[repos]]\nname = "redis"\ngithub = "redis/redis"\n'
    with pytest.raises(ConfigurationError, match="listed twice"):
        SettingsLoader().load(write_config(doubled), ExternalSettings)


@pytest.mark.parametrize("github", ["redis", "redis/redis/extra", "https://github.com/redis/redis"])
def test_github_name_must_be_owner_slash_repo(github: str) -> None:
    with pytest.raises(ValueError, match="github"):
        ExternalRepoSpec(name="x", github=github)


@pytest.mark.parametrize("gitlab_path", ["redis", "/group/redis", "group/redis/"])
def test_gitlab_path_needs_a_group(gitlab_path: str) -> None:
    with pytest.raises(ValueError, match="gitlab_path"):
        InternalRepoSpec(name="x", gitlab_path=gitlab_path)


@pytest.mark.parametrize(
    ("asset_filter", "file_name", "wanted"),
    [
        ([], "Redis-Insight.dmg", True),
        (["win", "linux"], "Redis-Insight-win-installer.exe", True),
        (["win", "linux"], "Redis-Insight-mac-arm64.dmg", False),
        (["LINUX"], "redis-insight-linux.AppImage", True),
    ],
)
def test_asset_filter_matches_by_keyword(asset_filter: list[str], file_name: str, wanted: bool) -> None:
    assert ExternalRepoSpec(name="x", github="o/r", asset_filter=asset_filter).wants_asset(file_name) is wanted


def test_pick_keeps_everything_without_names() -> None:
    specs: list[ExternalRepoSpec] = [ExternalRepoSpec(name="a", github="o/a"), ExternalRepoSpec(name="b", github="o/b")]
    assert pick(specs, []) == specs


def test_pick_narrows_to_the_named_repositories() -> None:
    specs: list[ExternalRepoSpec] = [ExternalRepoSpec(name="a", github="o/a"), ExternalRepoSpec(name="b", github="o/b")]
    assert [spec.name for spec in pick(specs, ["b"])] == ["b"]


def test_pick_refuses_unknown_names() -> None:
    with pytest.raises(ConfigurationError, match="nope"):
        pick([ExternalRepoSpec(name="a", github="o/a")], ["nope"])
