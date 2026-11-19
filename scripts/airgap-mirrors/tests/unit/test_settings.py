from pathlib import Path

import pytest

from airgap_mirrors.exceptions import ConfigurationError
from airgap_mirrors.settings import (
    Architecture,
    AssetPolicy,
    AssetPolicyKind,
    ExternalRepoSpec,
    ExternalSettings,
    InternalRepoSpec,
    InternalSettings,
    Platform,
    SettingsLoader,
    architecture_of,
    pick,
)

EXTERNAL_TOML: str = """
mirrors_dir = "/m"
transfer_dir = "/t"
github_url = "https://github.com"
github_api_url = "https://api.github.com"
http_timeout_seconds = 30
download_attempts = 3
default_assets = "latest-per-type"
default_platforms = ["windows", "linux", "redhat"]
default_architectures = ["x86_64"]
excluded_asset_suffixes = [".asc", ".sig"]

[[repos]]
name = "redis"
github = "redis/redis"
"""

INTERNAL_TOML: str = """
mirrors_dir = "/m"
transfer_dir = "/t"
gitlab_url = "https://gitlab.example"
gitlab_group = "group/sub"
release_package_name = "release-assets"
http_timeout_seconds = 30
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
    assert settings.push_url(settings.spec_for("redis")) == "https://gitlab.example/group/sub/redis.git"


def test_push_url_uses_the_ssh_base_when_set(write_config, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GITLAB_TOKEN", "t")
    text: str = INTERNAL_TOML + 'git_remote_base = "ssh://git@gitlab.example"\n'
    settings: InternalSettings = SettingsLoader().load(write_config(text), InternalSettings)
    assert settings.push_url(settings.spec_for("redis")) == "ssh://git@gitlab.example/group/sub/redis.git"


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


def test_repository_takes_the_default_policy(write_config) -> None:
    settings: ExternalSettings = SettingsLoader().load(write_config(EXTERNAL_TOML), ExternalSettings)
    assert settings.repos[0].asset_policy == AssetPolicy(kind=AssetPolicyKind.LATEST_PER_TYPE)


def test_repository_takes_the_default_platforms(write_config) -> None:
    settings: ExternalSettings = SettingsLoader().load(write_config(EXTERNAL_TOML), ExternalSettings)
    assert settings.repos[0].platforms == [Platform.WINDOWS, Platform.LINUX, Platform.REDHAT]


def test_repository_keeps_its_own_policy(write_config) -> None:
    text: str = EXTERNAL_TOML + 'assets = "none"\n'
    settings: ExternalSettings = SettingsLoader().load(write_config(text), ExternalSettings)
    assert settings.repos[0].asset_policy == AssetPolicy(kind=AssetPolicyKind.NONE)


def test_unknown_platform_is_refused(write_config) -> None:
    text: str = EXTERNAL_TOML.replace('"redhat"]', '"solaris"]')
    with pytest.raises(ConfigurationError, match="solaris"):
        SettingsLoader().load(write_config(text), ExternalSettings)


@pytest.mark.parametrize(
    ("file_name", "wanted"),
    [
        ("Redis-Insight-win-installer.exe", True),
        ("Redis-Insight-linux-x86_64.AppImage", True),
        ("Redis-Insight-linux-x86_64.rpm", True),
        ("memtier-benchmark-2.6.1-1.el9.x86_64.rpm", True),
        ("Redis-Insight-mac-arm64.dmg", False),
        ("memtier-benchmark-2.6.1-1.amzn2023.x86_64.rpm", False),
        ("redis-full-8.12-rc3.tar.gz", True),
        ("bundle.yaml", True),
    ],
)
def test_platform_filter_keeps_wanted_and_neutral_files(file_name: str, wanted: bool) -> None:
    spec: ExternalRepoSpec = ExternalRepoSpec(name="x", github="o/r", platforms=["windows", "linux", "redhat"])
    assert spec.wants_asset(file_name) is wanted


def test_no_platforms_keeps_every_file() -> None:
    assert ExternalRepoSpec(name="x", github="o/r", platforms=[]).wants_asset("tool-mac.dmg") is True


def test_repository_takes_the_default_architectures(write_config) -> None:
    settings: ExternalSettings = SettingsLoader().load(write_config(EXTERNAL_TOML), ExternalSettings)
    assert settings.repos[0].architectures == [Architecture.X86_64]


@pytest.mark.parametrize(
    ("file_name", "architecture"),
    [
        ("Redis-Insight-linux-aarch64.rpm", Architecture.ARM64),
        ("Redis-Insight-linux-amd64.deb", Architecture.X86_64),
        ("redisctl-x86_64-unknown-linux-musl.tar.xz", Architecture.X86_64),
        ("tool_bookworm_armhf.deb", Architecture.ARM32),
        ("tool_bookworm_i386.deb", Architecture.X86_32),
        ("Redis-Insight-win-installer.exe", None),
        ("redisctl-installer.sh", None),
    ],
)
def test_architecture_is_read_from_the_file_name(file_name: str, architecture: Architecture | None) -> None:
    assert architecture_of(file_name) == architecture


@pytest.mark.parametrize(
    ("file_name", "wanted"),
    [
        ("Redis-Insight-linux-x86_64.AppImage", True),
        ("Redis-Insight-linux-arm64.AppImage", False),
        ("Redis-Insight-win-installer.exe", True),
    ],
)
def test_architecture_filter_keeps_x86_64_and_neutral_files(file_name: str, wanted: bool) -> None:
    spec: ExternalRepoSpec = ExternalRepoSpec(name="x", github="o/r", architectures=["x86_64"])
    assert spec.wants_asset(file_name) is wanted


def test_repository_takes_the_excluded_suffixes(write_config) -> None:
    settings: ExternalSettings = SettingsLoader().load(write_config(EXTERNAL_TOML), ExternalSettings)
    assert settings.repos[0].excluded_suffixes == [".asc", ".sig"]


@pytest.mark.parametrize(
    ("file_name", "wanted"),
    [
        ("riotx-standalone-1.15.4-linux-x86_64.zip.asc", False),
        ("tool-linux-x86_64.tar.gz.SIG", False),
        ("riotx-standalone-1.15.4-linux-x86_64.zip", True),
        ("tool-linux-x86_64.tar.gz.sha256", True),
        ("ascii-tool-linux-x86_64.zip", True),
    ],
)
def test_excluded_suffix_drops_the_file(file_name: str, wanted: bool) -> None:
    spec: ExternalRepoSpec = ExternalRepoSpec(name="x", github="o/r", excluded_suffixes=[".asc", ".sig"])
    assert spec.wants_asset(file_name) is wanted


def test_home_folder_in_paths_is_expanded(write_config) -> None:
    text: str = EXTERNAL_TOML.replace('mirrors_dir = "/m"', 'mirrors_dir = "~/airgap/mirrors"')
    settings: ExternalSettings = SettingsLoader().load(write_config(text), ExternalSettings)
    assert settings.mirrors_dir == Path.home() / "airgap" / "mirrors"


def test_external_example_config_loads_as_it_is() -> None:
    loaded: ExternalSettings = SettingsLoader().load(Path("config/external.toml.example"), ExternalSettings)
    assert len(loaded.repos) == 34


def test_internal_example_config_needs_only_the_group_filled_in(monkeypatch: pytest.MonkeyPatch, write_config) -> None:
    monkeypatch.setenv("GITLAB_TOKEN", "t")
    text: str = Path("config/internal.toml.example").read_text().replace("<your-group>", "redis")
    text = text.replace("gitlab.<your-company>.example", "gitlab.example")
    loaded: InternalSettings = SettingsLoader().load(write_config(text), InternalSettings)
    assert loaded.spec_for("redis").gitlab_path == "redis/mirrors/redis"
