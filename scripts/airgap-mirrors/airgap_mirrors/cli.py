import argparse
import logging
from collections.abc import Sequence
from pathlib import Path

from airgap_mirrors.composition import Composition
from airgap_mirrors.exceptions import ConfigurationError
from airgap_mirrors.logging_setup import LoggingSetup
from airgap_mirrors.settings import ExternalSettings, InternalSettings, SettingsLoader, pick

logger: logging.Logger = logging.getLogger("airgap_mirrors")

TOOL_DIR: Path = Path(__file__).resolve().parent.parent
DEFAULT_LOGGING_CONFIG: Path = TOOL_DIR / "config" / "logging.toml"

EXIT_OK: int = 0
EXIT_SOME_FAILED: int = 1
EXIT_BAD_CONFIG: int = 2


def build_parser() -> argparse.ArgumentParser:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="python -m airgap_mirrors",
        description="Copy GitHub repositories to an air-gapped GitLab over a USB stick.",
    )
    parser.add_argument("--config", type=Path, required=True, help="this machine's TOML config")
    parser.add_argument("--logging-config", type=Path, default=DEFAULT_LOGGING_CONFIG)
    commands = parser.add_subparsers(dest="command", required=True)

    export = commands.add_parser("export", help="online machine: fetch from GitHub and write the transfer folder")
    export.add_argument("--repo", action="append", default=[], help="only this repository (repeatable)")
    export.add_argument("--skip-releases", action="store_true", help="git only, no release notes or files")
    export.add_argument("--full", action="store_true", help="send everything again, not just what is new")

    commands.add_parser("confirm", help="online machine: read the receipt the import wrote")

    imported = commands.add_parser("import", help="air-gapped machine: load the transfer folder into GitLab")
    imported.add_argument("--repo", action="append", default=[], help="only this repository (repeatable)")
    imported.add_argument("--skip-releases", action="store_true", help="git only, no releases")
    return parser


def main(argv: Sequence[str] | None = None, composition: Composition | None = None) -> int:
    arguments: argparse.Namespace = build_parser().parse_args(argv)
    builder: Composition = composition or Composition()
    try:
        LoggingSetup(arguments.logging_config).apply()
        failed: list[str] = _dispatch(arguments, builder, SettingsLoader())
    except ConfigurationError as invalid:
        logger.critical("%s", invalid)
        return EXIT_BAD_CONFIG
    if failed:
        logger.error("finished with failures: %s", ", ".join(failed))
        return EXIT_SOME_FAILED
    return EXIT_OK


def _dispatch(arguments: argparse.Namespace, builder: Composition, loader: SettingsLoader) -> list[str]:
    if arguments.command == "import":
        internal: InternalSettings = loader.load(arguments.config, InternalSettings)
        command = builder.import_command(internal, with_releases=not arguments.skip_releases)
        return command.run(pick(internal.repos, arguments.repo))
    external: ExternalSettings = loader.load(arguments.config, ExternalSettings)
    if arguments.command == "confirm":
        return builder.confirm_command(external).run()
    export = builder.export_command(external, with_releases=not arguments.skip_releases)
    return export.run(pick(external.repos, arguments.repo), full=arguments.full)
