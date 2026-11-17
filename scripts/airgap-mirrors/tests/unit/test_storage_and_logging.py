import logging
from pathlib import Path

import pytest

from airgap_mirrors.exceptions import ConfigurationError, TransferError
from airgap_mirrors.logging_setup import LoggingSetup
from airgap_mirrors.models import ImportLedger
from airgap_mirrors.storage import JsonModelStore, LedgerLocator


def test_saved_model_loads_back(tmp_path: Path) -> None:
    store: JsonModelStore = JsonModelStore()
    store.save(tmp_path / "deep" / "ledger.json", ImportLedger(applied_state_ids=["a"]))
    assert store.load(tmp_path / "deep" / "ledger.json", ImportLedger) == ImportLedger(applied_state_ids=["a"])


def test_missing_file_loads_as_nothing(tmp_path: Path) -> None:
    assert JsonModelStore().load(tmp_path / "absent.json", ImportLedger) is None


def test_damaged_file_is_reported(tmp_path: Path) -> None:
    (tmp_path / "ledger.json").write_text("{not json")
    with pytest.raises(TransferError, match="damaged"):
        JsonModelStore().load(tmp_path / "ledger.json", ImportLedger)


def test_save_leaves_no_temporary_files(tmp_path: Path) -> None:
    JsonModelStore().save(tmp_path / "ledger.json", ImportLedger())
    assert [path.name for path in tmp_path.iterdir()] == ["ledger.json"]


@pytest.mark.parametrize(
    ("method", "expected"),
    [
        ("repository_path", "redis.git"),
        ("export_ledger", "redis.export-ledger.json"),
        ("import_ledger", "redis.import-ledger.json"),
    ],
)
def test_ledger_locations(tmp_path: Path, method: str, expected: str) -> None:
    assert getattr(LedgerLocator(tmp_path), method)("redis") == tmp_path / expected


def test_logging_config_sets_the_level(tmp_path: Path) -> None:
    config: Path = tmp_path / "logging.toml"
    config.write_text('version = 1\ndisable_existing_loggers = false\n[loggers.airgap_mirrors]\nlevel = "DEBUG"\n')
    LoggingSetup(config).apply()
    assert logging.getLogger("airgap_mirrors").level == logging.DEBUG


def test_missing_logging_config_is_reported(tmp_path: Path) -> None:
    with pytest.raises(ConfigurationError, match="not found"):
        LoggingSetup(tmp_path / "absent.toml").apply()


def test_invalid_logging_config_is_reported(tmp_path: Path) -> None:
    config: Path = tmp_path / "logging.toml"
    config.write_text("version = 99\n")
    with pytest.raises(ConfigurationError, match="invalid"):
        LoggingSetup(config).apply()
