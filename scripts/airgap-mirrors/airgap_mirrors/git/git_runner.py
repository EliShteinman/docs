import logging
import os
import subprocess
from collections.abc import Mapping
from pathlib import Path

from airgap_mirrors.exceptions import GitCommandError

logger: logging.Logger = logging.getLogger(__name__)


class GitRunner:
    """Runs git. Extra configuration (such as an auth header) goes in through the environment, never the arguments,
    so it never shows up in a process list or a log line."""

    def __init__(self, executable: str = "git", config: Mapping[str, str] | None = None) -> None:
        self._executable: str = executable
        self._environment: dict[str, str] = _environment_with_config(config or {})

    def run(self, arguments: list[str], *, cwd: Path | None = None, stdin: str | None = None) -> str:
        logger.debug("git %s", " ".join(arguments))
        completed: subprocess.CompletedProcess[str] = subprocess.run(
            [self._executable, *arguments],
            cwd=cwd,
            input=stdin,
            capture_output=True,
            text=True,
            env=self._environment,
            check=False,
        )
        if completed.returncode != 0:
            raise GitCommandError(arguments, completed.returncode, completed.stderr)
        return completed.stdout

    def succeeds(self, arguments: list[str], *, cwd: Path | None = None) -> bool:
        completed: subprocess.CompletedProcess[bytes] = subprocess.run(
            [self._executable, *arguments],
            cwd=cwd,
            capture_output=True,
            env=self._environment,
            check=False,
        )
        return completed.returncode == 0


def _environment_with_config(config: Mapping[str, str]) -> dict[str, str]:
    environment: dict[str, str] = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}
    environment["GIT_CONFIG_COUNT"] = str(len(config))
    for index, (key, value) in enumerate(config.items()):
        environment[f"GIT_CONFIG_KEY_{index}"] = key
        environment[f"GIT_CONFIG_VALUE_{index}"] = value
    return environment
