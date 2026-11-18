from pathlib import Path


class LedgerLocator:
    """Each machine keeps one small JSON ledger per repository next to its copy of that repository."""

    def __init__(self, mirrors_dir: Path) -> None:
        self._mirrors_dir: Path = mirrors_dir

    def repository_path(self, repository: str) -> Path:
        return self._mirrors_dir / f"{repository}.git"

    def export_ledger(self, repository: str) -> Path:
        return self._mirrors_dir / f"{repository}.export-ledger.json"

    def import_ledger(self, repository: str) -> Path:
        return self._mirrors_dir / f"{repository}.import-ledger.json"

    @property
    def published_projects(self) -> Path:
        return self._mirrors_dir / "published-projects.json"

    @property
    def helm_values(self) -> Path:
        return self._mirrors_dir / "helm-values-git-mirrors.yaml"
