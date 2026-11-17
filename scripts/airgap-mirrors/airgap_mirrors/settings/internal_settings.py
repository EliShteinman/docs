from pathlib import Path

from pydantic import AliasChoices, Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from airgap_mirrors.settings.repo_list import require_unique_names
from airgap_mirrors.settings.repo_specs import InternalRepoSpec


class InternalSettings(BaseSettings):
    """The air-gapped machine: where GitLab is and which project holds each repository."""

    model_config = SettingsConfigDict(extra="forbid", env_prefix="AIRGAP_MIRRORS_")

    mirrors_dir: Path
    transfer_dir: Path
    gitlab_url: str = Field(pattern=r"^https?://")
    git_remote_base: str | None = None
    ca_file: Path | None = None
    release_package_name: str = Field(pattern=r"^[A-Za-z0-9._-]+$")
    http_timeout_seconds: float = Field(gt=0)
    gitlab_token: SecretStr = Field(validation_alias=AliasChoices("GITLAB_TOKEN"))
    repos: list[InternalRepoSpec] = Field(min_length=1)

    @field_validator("repos")
    @classmethod
    def _unique(cls, repos: list[InternalRepoSpec]) -> list[InternalRepoSpec]:
        return require_unique_names(repos)

    def push_url(self, spec: InternalRepoSpec) -> str:
        base: str = (self.git_remote_base or self.gitlab_url).rstrip("/")
        return f"{base}/{spec.gitlab_path}.git"
