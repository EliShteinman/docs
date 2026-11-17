from pathlib import Path
from typing import Annotated

from pydantic import AliasChoices, BeforeValidator, Field, SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from airgap_mirrors.settings.asset_policy import AssetPolicy
from airgap_mirrors.settings.platform import Platform
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
    default_assets: Annotated[AssetPolicy, BeforeValidator(AssetPolicy.from_text)]
    default_platforms: list[Platform] = Field(default_factory=list)
    repos: list[ExternalRepoSpec] = Field(min_length=1)

    @field_validator("repos")
    @classmethod
    def _unique(cls, repos: list[ExternalRepoSpec]) -> list[ExternalRepoSpec]:
        return require_unique_names(repos)

    @model_validator(mode="after")
    def _apply_defaults(self) -> "ExternalSettings":
        self.repos = [spec.with_defaults(self.default_assets, self.default_platforms) for spec in self.repos]
        return self

    def upstream_url(self, spec: ExternalRepoSpec) -> str:
        return f"{self.github_url.rstrip('/')}/{spec.github}"
