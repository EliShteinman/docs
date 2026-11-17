import logging
import tomllib
from pathlib import Path
from typing import TypeVar

from pydantic import ValidationError
from pydantic_settings import BaseSettings

from airgap_mirrors.exceptions import ConfigurationError

SettingsT = TypeVar("SettingsT", bound=BaseSettings)

logger: logging.Logger = logging.getLogger(__name__)


class SettingsLoader:
    """Reads a TOML config file; tokens come from the environment, never from the file."""

    def load(self, path: Path, settings_type: type[SettingsT]) -> SettingsT:
        logger.debug("reading config %s", path)
        try:
            with path.open("rb") as config_file:
                values: dict[str, object] = tomllib.load(config_file)
        except FileNotFoundError as missing:
            raise ConfigurationError(f"config file not found: {path}") from missing
        except tomllib.TOMLDecodeError as broken:
            raise ConfigurationError(f"{path} is not valid TOML: {broken}") from broken
        try:
            return settings_type(**values)
        except ValidationError as invalid:
            raise ConfigurationError(f"{path}:\n{invalid}") from invalid
