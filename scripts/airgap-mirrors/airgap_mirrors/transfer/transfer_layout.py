from datetime import datetime
from pathlib import Path

MANIFEST_SUFFIX: str = ".manifest.json"
BUNDLE_SUFFIX: str = ".bundle"


class TransferLayout:
    """Where everything sits in the folder that travels on the USB stick.

    <transfer>/git/<repo>/<stamp>.manifest.json   what the repository must look like after this transfer
    <transfer>/git/<repo>/<stamp>.bundle          the new commits (absent when only refs moved)
    <transfer>/releases/<repo>/releases.json      release notes
    <transfer>/releases/<repo>/assets/<tag>/...   release files
    <transfer>/extra/<repo>/<path in the repo>    files the repository needs but does not keep in git
    """

    def __init__(self, root: Path) -> None:
        self.root: Path = root

    def git_dir(self, repository: str) -> Path:
        return self.root / "git" / repository

    def manifest_path(self, repository: str, created_at: datetime) -> Path:
        return self.git_dir(repository) / f"{_stamp(created_at)}{MANIFEST_SUFFIX}"

    def bundle_path(self, repository: str, created_at: datetime) -> Path:
        return self.git_dir(repository) / f"{_stamp(created_at)}{BUNDLE_SUFFIX}"

    def manifest_paths(self, repository: str) -> list[Path]:
        directory: Path = self.git_dir(repository)
        if not directory.is_dir():
            return []
        return sorted(directory.glob(f"*{MANIFEST_SUFFIX}"))

    def repository_names(self) -> list[str]:
        """Every repository the transfer folder carries something for."""
        found: set[str] = set()
        for kind in ("git", "releases", "extra"):
            directory: Path = self.root / kind
            if directory.is_dir():
                found.update(child.name for child in directory.iterdir() if child.is_dir())
        return sorted(found)

    def releases_file(self, repository: str) -> Path:
        return self.root / "releases" / repository / "releases.json"

    def asset_dir(self, repository: str, tag: str) -> Path:
        return self.root / "releases" / repository / "assets" / tag

    def extra_dir(self, repository: str) -> Path:
        return self.root / "extra" / repository

    def extra_file(self, repository: str, path: str) -> Path:
        return self.extra_dir(repository) / path


def _stamp(moment: datetime) -> str:
    return moment.strftime("%Y%m%dT%H%M%S%fZ")
