import hashlib
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from pydantic import ValidationError
from pytest_mock import MockerFixture

from airgap_mirrors.exceptions import ExtraFileDownloadError
from airgap_mirrors.external import ExtraFileExporter
from airgap_mirrors.http import HttpClient
from airgap_mirrors.internal import ExtraFileImporter, GitLabClient
from airgap_mirrors.models import UploadedExtraFiles
from airgap_mirrors.settings import ExternalRepoSpec, ExtraFile, InternalRepoSpec
from airgap_mirrors.storage import JsonModelStore, LedgerLocator
from airgap_mirrors.transfer import TransferLayout

MODEL: ExtraFile = ExtraFile(url="https://models.test/model.onnx", path="src/Resources/model.onnx")
VOCAB: ExtraFile = ExtraFile(url="https://models.test/vocab.txt", path="src/Resources/vocab.txt")
SPEC: ExternalRepoSpec = ExternalRepoSpec(name="om", github="o/om", extra_files=[MODEL, VOCAB])
INTERNAL: InternalRepoSpec = InternalRepoSpec(name="om", gitlab_path="g/om")


@pytest.mark.parametrize("path", ["/etc/passwd", "../outside.bin", "src/../../x", "src\\model.onnx", "./model.onnx"])
def test_extra_file_path_must_stay_inside_the_repository(path: str) -> None:
    with pytest.raises(ValidationError):
        ExtraFile(url="https://models.test/x", path=path)


def test_extra_file_url_must_be_http() -> None:
    with pytest.raises(ValidationError):
        ExtraFile(url="ftp://models.test/x", path="x")


def test_extra_files_with_the_same_file_name_are_refused() -> None:
    twin: ExtraFile = ExtraFile(url="https://models.test/other", path="other/model.onnx")
    with pytest.raises(ValidationError, match=r"model\.onnx"):
        ExternalRepoSpec(name="om", github="o/om", extra_files=[MODEL, twin])


@pytest.fixture
def layout(tmp_path: Path) -> TransferLayout:
    return TransferLayout(tmp_path / "transfer")


@pytest.fixture
def ledgers(tmp_path: Path) -> LedgerLocator:
    return LedgerLocator(tmp_path / "ledgers")


@pytest.fixture
def http(mocker: MockerFixture) -> MagicMock:
    client: MagicMock = mocker.create_autospec(HttpClient, instance=True)
    client.download.side_effect = lambda _url, target: (
        target.parent.mkdir(parents=True, exist_ok=True),
        target.write_bytes(b"weights"),
    )
    return client


@pytest.fixture
def exporter(http: MagicMock, layout: TransferLayout, ledgers: LedgerLocator) -> ExtraFileExporter:
    return ExtraFileExporter(http, layout, ledgers, JsonModelStore())


def test_exporter_puts_each_file_at_its_repository_path(
    exporter: ExtraFileExporter, http: MagicMock, layout: TransferLayout
) -> None:
    exporter.export(SPEC)
    assert http.download.call_args_list[0].args == (MODEL.url, layout.extra_dir("om") / "src/Resources/model.onnx")


def test_exporter_counts_the_files_it_downloaded(exporter: ExtraFileExporter) -> None:
    assert exporter.export(SPEC) == 2


def test_exporter_does_nothing_for_a_repository_without_extra_files(
    exporter: ExtraFileExporter, http: MagicMock
) -> None:
    exporter.export(ExternalRepoSpec(name="plain", github="o/plain"))
    http.download.assert_not_called()


def test_exporter_does_not_send_a_file_twice(exporter: ExtraFileExporter) -> None:
    exporter.export(SPEC)
    assert exporter.export(SPEC) == 0


def test_full_export_sends_the_files_again(exporter: ExtraFileExporter) -> None:
    exporter.export(SPEC)
    assert exporter.export(SPEC, full=True) == 2


def test_a_changed_url_is_sent_again(exporter: ExtraFileExporter) -> None:
    exporter.export(SPEC)
    moved: ExtraFile = MODEL.model_copy(update={"url": "https://models.test/v2/model.onnx"})
    assert exporter.export(SPEC.model_copy(update={"extra_files": [moved, VOCAB]})) == 1


def test_a_failed_download_is_tried_again_next_export(exporter: ExtraFileExporter, http: MagicMock) -> None:
    http.download.side_effect = [None, ExtraFileDownloadError(0, VOCAB.url, "dropped")]
    with pytest.raises(ExtraFileDownloadError):
        exporter.export(SPEC)
    http.download.side_effect = None
    assert exporter.export(SPEC) == 1


@pytest.fixture
def gitlab(mocker: MockerFixture) -> MagicMock:
    client: MagicMock = mocker.create_autospec(GitLabClient, instance=True)
    client.upload_package_file.return_value = "https://gl/package/file"
    return client


@pytest.fixture
def importer(gitlab: MagicMock, layout: TransferLayout, ledgers: LedgerLocator) -> ExtraFileImporter:
    return ExtraFileImporter(gitlab, layout, ledgers, JsonModelStore(), "extra-files", "latest")


@pytest.fixture
def staged(layout: TransferLayout) -> Path:
    model: Path = layout.extra_file("om", MODEL.path)
    model.parent.mkdir(parents=True)
    model.write_bytes(b"weights")
    (model.parent / ".model.onnx.partial").write_bytes(b"w")
    return model


def test_importer_does_nothing_without_extra_files(importer: ExtraFileImporter, gitlab: MagicMock) -> None:
    importer.import_repository(INTERNAL)
    gitlab.upload_package_file.assert_not_called()


def test_importer_uploads_each_file_to_the_package(
    importer: ExtraFileImporter, gitlab: MagicMock, staged: Path
) -> None:
    importer.import_repository(INTERNAL)
    gitlab.upload_package_file.assert_called_once_with("g/om", "extra-files", "latest", staged)


def test_importer_records_the_uploaded_content(
    importer: ExtraFileImporter, ledgers: LedgerLocator, staged: Path
) -> None:
    importer.import_repository(INTERNAL)
    recorded: UploadedExtraFiles | None = JsonModelStore().load(ledgers.uploaded_extra_files("om"), UploadedExtraFiles)
    assert recorded == UploadedExtraFiles(digests={MODEL.path: hashlib.sha256(b"weights").hexdigest()})


def test_importer_run_twice_uploads_once(importer: ExtraFileImporter, staged: Path) -> None:
    importer.import_repository(INTERNAL)
    assert importer.import_repository(INTERNAL) == 0


def test_importer_uploads_a_changed_file_again(importer: ExtraFileImporter, staged: Path) -> None:
    importer.import_repository(INTERNAL)
    staged.write_bytes(b"new weights")
    assert importer.import_repository(INTERNAL) == 1
