from typing import Annotated

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field

from airgap_mirrors.settings.architecture import Architecture, architecture_of
from airgap_mirrors.settings.asset_policy import AssetPolicy
from airgap_mirrors.settings.platform import Platform, platform_of

RepositoryName = Annotated[str, Field(pattern=r"^[A-Za-z0-9._-]+$")]


class ExternalRepoSpec(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    name: RepositoryName
    github: str = Field(pattern=r"^[A-Za-z0-9._-]+/[A-Za-z0-9._-]+$")
    assets: Annotated[AssetPolicy | None, BeforeValidator(AssetPolicy.from_text)] = None
    platforms: list[Platform] | None = None
    architectures: list[Architecture] | None = None
    asset_filter: list[str] = Field(default_factory=list)
    excluded_suffixes: list[str] = Field(default_factory=list)

    def with_defaults(
        self,
        assets: AssetPolicy,
        platforms: list[Platform],
        architectures: list[Architecture],
        excluded_suffixes: list[str],
    ) -> "ExternalRepoSpec":
        return self.model_copy(
            update={
                "assets": self.assets if self.assets is not None else assets,
                "platforms": self.platforms if self.platforms is not None else platforms,
                "architectures": self.architectures if self.architectures is not None else architectures,
                "excluded_suffixes": excluded_suffixes,
            }
        )

    @property
    def asset_policy(self) -> AssetPolicy:
        return self.assets if self.assets is not None else AssetPolicy()

    def wants_asset(self, file_name: str) -> bool:
        return (
            self._suffix_allowed(file_name)
            and self._platform_wanted(file_name)
            and self._architecture_wanted(file_name)
            and self._keyword_wanted(file_name)
        )

    def _suffix_allowed(self, file_name: str) -> bool:
        lowered: str = file_name.lower()
        return not any(lowered.endswith(suffix.lower()) for suffix in self.excluded_suffixes)

    def _platform_wanted(self, file_name: str) -> bool:
        if not self.platforms:
            return True
        platform: Platform | None = platform_of(file_name)
        return platform is None or platform in self.platforms

    def _architecture_wanted(self, file_name: str) -> bool:
        if not self.architectures:
            return True
        architecture: Architecture | None = architecture_of(file_name)
        return architecture is None or architecture in self.architectures

    def _keyword_wanted(self, file_name: str) -> bool:
        if not self.asset_filter:
            return True
        lowered: str = file_name.lower()
        return any(keyword.lower() in lowered for keyword in self.asset_filter)


class InternalRepoSpec(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    name: RepositoryName
    gitlab_path: str = Field(pattern=r"^[A-Za-z0-9._-]+(/[A-Za-z0-9._-]+)+$")
