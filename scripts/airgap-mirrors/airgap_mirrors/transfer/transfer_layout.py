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
    <transfer>/receipt.json                       written by import, read by confirm
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

    def releases_file(self, repository: str) -> Path:
        return self.root / "releases" / repository / "releases.json"

    def asset_dir(self, repository: str, tag: str) -> Path:
        return self.root / "releases" / repository / "assets" / tag

    @property
    def receipt_path(self) -> Path:
        return self.root / "receipt.json"


def _stamp(moment: datetime) -> str:
    return moment.strftime("%Y%m%dT%H%M%S%fZ")
