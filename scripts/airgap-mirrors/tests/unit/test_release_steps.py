from pathlib import Path
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from airgap_mirrors.external import GitHubClient, ReleaseExporter
from airgap_mirrors.internal import GitLabClient, ReleaseImporter, package_version
from airgap_mirrors.models import ReleaseAsset, ReleaseCatalog, ReleaseRecord
from airgap_mirrors.settings import ExternalRepoSpec, InternalRepoSpec
from airgap_mirrors.storage import JsonModelStore, LedgerLocator
from airgap_mirrors.transfer import TransferLayout

RELEASE: ReleaseRecord = ReleaseRecord(
    tag_name="v1.0",
    assets=[
        ReleaseAsset(name="tool-linux.tar.gz", size=3, browser_download_url="https://dl/linux"),
        ReleaseAsset(name="tool-mac.dmg", size=3, browser_download_url="https://dl/mac"),
    ],
)


@pytest.fixture
def layout(tmp_path: Path) -> TransferLayout:
    return TransferLayout(tmp_path)


def exporter(github: MagicMock, layout: TransferLayout) -> ReleaseExporter:
    return ReleaseExporter(github, layout, LedgerLocator(layout.root / "ledgers"), JsonModelStore())


@pytest.fixture
def github(mocker: MockerFixture) -> MagicMock:
    client: MagicMock = mocker.create_autospec(GitHubClient, instance=True)
    client.published_releases.return_value = [RELEASE]
    client.download.side_effect = lambda _url, target: (
        target.parent.mkdir(parents=True, exist_ok=True),
        target.write_bytes(b"abc"),
    )
    return client


def test_exporter_writes_the_release_notes(github: MagicMock, layout: TransferLayout) -> None:
    exporter(github, layout).export(ExternalRepoSpec(name="tool", github="o/tool", assets="none"))
    assert JsonModelStore().load(layout.releases_file("tool"), ReleaseCatalog) == ReleaseCatalog(
        repository="o/tool", releases=[RELEASE]
    )


def test_exporter_downloads_nothing_under_policy_none(github: MagicMock, layout: TransferLayout) -> None:
    exporter(github, layout).export(ExternalRepoSpec(name="tool", github="o/tool", assets="none"))
    github.download.assert_not_called()


def test_exporter_downloads_only_filtered_files(github: MagicMock, layout: TransferLayout) -> None:
    spec: ExternalRepoSpec = ExternalRepoSpec(name="tool", github="o/tool", asset_filter=["linux"])
    exporter(github, layout).export(spec)
    github.download.assert_called_once_with("https://dl/linux", layout.asset_dir("tool", "v1.0") / "tool-linux.tar.gz")


def test_exporter_skips_a_file_already_downloaded(github: MagicMock, layout: TransferLayout) -> None:
    spec: ExternalRepoSpec = ExternalRepoSpec(name="tool", github="o/tool", asset_filter=["linux"])
    target: Path = layout.asset_dir("tool", "v1.0") / "tool-linux.tar.gz"
    target.parent.mkdir(parents=True)
    target.write_bytes(b"abc")
    assert exporter(github, layout).export(spec) == 0


def test_exporter_downloads_again_when_the_size_is_wrong(github: MagicMock, layout: TransferLayout) -> None:
    spec: ExternalRepoSpec = ExternalRepoSpec(name="tool", github="o/tool", asset_filter=["linux"])
    target: Path = layout.asset_dir("tool", "v1.0") / "tool-linux.tar.gz"
    target.parent.mkdir(parents=True)
    target.write_bytes(b"a")
    assert exporter(github, layout).export(spec) == 1


def test_exporter_does_not_send_a_file_twice(github: MagicMock, layout: TransferLayout) -> None:
    spec: ExternalRepoSpec = ExternalRepoSpec(name="tool", github="o/tool", asset_filter=["linux"])
    exporter(github, layout).export(spec)
    for leftover in layout.asset_dir("tool", "v1.0").iterdir():
        leftover.unlink()
    assert exporter(github, layout).export(spec) == 0


def test_full_export_sends_a_file_again(github: MagicMock, layout: TransferLayout) -> None:
    spec: ExternalRepoSpec = ExternalRepoSpec(name="tool", github="o/tool", asset_filter=["linux"])
    exporter(github, layout).export(spec)
    for leftover in layout.asset_dir("tool", "v1.0").iterdir():
        leftover.unlink()
    assert exporter(github, layout).export(spec, full=True) == 1


SPEC: InternalRepoSpec = InternalRepoSpec(name="tool", gitlab_path="g/tool")


@pytest.fixture
def gitlab(mocker: MockerFixture) -> MagicMock:
    client: MagicMock = mocker.create_autospec(GitLabClient, instance=True)
    client.tag_exists.return_value = True
    client.release_exists.return_value = False
    client.release_link_names.return_value = set()
    client.upload_package_file.return_value = "https://gl/package/file"
    return client


@pytest.fixture
def staged(layout: TransferLayout) -> TransferLayout:
    JsonModelStore().save(layout.releases_file("tool"), ReleaseCatalog(repository="o/tool", releases=[RELEASE]))
    directory: Path = layout.asset_dir("tool", "v1.0")
    directory.mkdir(parents=True)
    (directory / "tool-linux.tar.gz").write_bytes(b"abc")
    (directory / ".tool-linux.tar.gz.partial").write_bytes(b"a")
    return layout


def importer(gitlab: MagicMock, layout: TransferLayout) -> ReleaseImporter:
    return ReleaseImporter(gitlab, layout, JsonModelStore(), "release-assets")


def test_importer_does_nothing_without_release_notes(gitlab: MagicMock, layout: TransferLayout) -> None:
    assert importer(gitlab, layout).import_repository(SPEC) == 0


def test_importer_skips_a_release_whose_tag_is_missing(gitlab: MagicMock, staged: TransferLayout) -> None:
    gitlab.tag_exists.return_value = False
    importer(gitlab, staged).import_repository(SPEC)
    gitlab.create_release.assert_not_called()


def test_importer_creates_a_missing_release(gitlab: MagicMock, staged: TransferLayout) -> None:
    importer(gitlab, staged).import_repository(SPEC)
    gitlab.create_release.assert_called_once_with("g/tool", RELEASE)


def test_importer_keeps_an_existing_release(gitlab: MagicMock, staged: TransferLayout) -> None:
    gitlab.release_exists.return_value = True
    importer(gitlab, staged).import_repository(SPEC)
    gitlab.create_release.assert_not_called()


def test_importer_uploads_and_links_each_file(gitlab: MagicMock, staged: TransferLayout) -> None:
    importer(gitlab, staged).import_repository(SPEC)
    gitlab.link_release_file.assert_called_once_with("g/tool", "v1.0", "tool-linux.tar.gz", "https://gl/package/file")


def test_importer_skips_files_already_linked(gitlab: MagicMock, staged: TransferLayout) -> None:
    gitlab.release_link_names.return_value = {"tool-linux.tar.gz"}
    assert importer(gitlab, staged).import_repository(SPEC) == 0


@pytest.mark.parametrize(
    ("tag", "version"), [("v7.2.4", "v7.2.4"), ("release/1.0", "release-1.0"), ("1.0+rc", "1.0+rc")]
)
def test_package_version_is_safe_for_gitlab(tag: str, version: str) -> None:
    assert package_version(tag) == version
