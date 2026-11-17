import logging.config
import tomllib
from pathlib import Path

from airgap_mirrors.exceptions import ConfigurationError


class LoggingSetup:
    def __init__(self, config_path: Path) -> None:
        self._config_path: Path = config_path

    def apply(self) -> None:
        try:
            with self._config_path.open("rb") as config_file:
                logging.config.dictConfig(tomllib.load(config_file))
        except FileNotFoundError as missing:
            raise ConfigurationError(f"logging config not found: {self._config_path}") from missing
        except (tomllib.TOMLDecodeError, ValueError) as broken:
            raise ConfigurationError(f"logging config {self._config_path} is invalid: {broken}") from broken
