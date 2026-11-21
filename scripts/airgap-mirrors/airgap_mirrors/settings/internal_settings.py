from enum import StrEnum
from pathlib import Path

from pydantic import AliasChoices, Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from airgap_mirrors.settings.repo_list import require_unique_names
from airgap_mirrors.settings.repo_specs import InternalRepoSpec


class ProjectVisibility(StrEnum):
    PRIVATE = "private"
    INTERNAL = "internal"
    PUBLIC = "public"


class InternalSettings(BaseSettings):
    """The air-gapped machine: where GitLab is and the group every copy goes into.

    Which repositories to import is read from the transfer folder, so no list is kept here. A project
    is <gitlab_group>/<repository name> unless a [[repos]] block names another path for it."""

    model_config = SettingsConfigDict(extra="forbid", env_prefix="AIRGAP_MIRRORS_")

    mirrors_dir: Path
    transfer_dir: Path
    gitlab_url: str = Field(pattern=r"^https?://")
    gitlab_group: str = Field(pattern=r"^[A-Za-z0-9._-]+(/[A-Za-z0-9._-]+)*$")
    project_visibility: ProjectVisibility | None = None
    git_remote_base: str | None = None
    ca_file: Path | None = None
    release_package_name: str = Field(pattern=r"^[A-Za-z0-9._-]+$")
    extra_files_package_name: str = Field(default="extra-files", pattern=r"^[A-Za-z0-9._-]+$")
    extra_files_package_version: str = Field(default="latest", pattern=r"^[A-Za-z0-9._+-]+$")
    http_timeout_seconds: float = Field(gt=0)
    gitlab_token: SecretStr = Field(validation_alias=AliasChoices("GITLAB_TOKEN"))
    repos: list[InternalRepoSpec] = Field(default_factory=list)

    @field_validator("mirrors_dir", "transfer_dir")
    @classmethod
    def _expand_home(cls, path: Path) -> Path:
        return path.expanduser()

    @field_validator("repos")
    @classmethod
    def _unique(cls, repos: list[InternalRepoSpec]) -> list[InternalRepoSpec]:
        return require_unique_names(repos)

    def spec_for(self, repository: str) -> InternalRepoSpec:
        for spec in self.repos:
            if spec.name == repository:
                return spec
        return InternalRepoSpec(name=repository, gitlab_path=f"{self.gitlab_group}/{repository}")

    def push_url(self, spec: InternalRepoSpec) -> str:
        base: str = (self.git_remote_base or self.gitlab_url).rstrip("/")
        return f"{base}/{spec.gitlab_path}.git"
