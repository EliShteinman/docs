from pathlib import Path

from pydantic import AliasChoices, Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from airgap_mirrors.settings.repo_list import require_unique_names
from airgap_mirrors.settings.repo_specs import ExternalRepoSpec


class ExternalSettings(BaseSettings):
    """The online machine. Holds nothing about the internal network."""

    model_config = SettingsConfigDict(extra="forbid", env_prefix="AIRGAP_MIRRORS_")

    mirrors_dir: Path
    transfer_dir: Path
    github_url: str = Field(pattern=r"^(https?|file)://")
    github_api_url: str = Field(pattern=r"^https?://")
    http_timeout_seconds: float = Field(gt=0)
    github_token: SecretStr | None = Field(default=None, validation_alias=AliasChoices("GITHUB_TOKEN"))
    repos: list[ExternalRepoSpec] = Field(min_length=1)

    @field_validator("repos")
    @classmethod
    def _unique(cls, repos: list[ExternalRepoSpec]) -> list[ExternalRepoSpec]:
        return require_unique_names(repos)

    def upstream_url(self, spec: ExternalRepoSpec) -> str:
        return f"{self.github_url.rstrip('/')}/{spec.github}"
