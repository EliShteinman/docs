from typing import Annotated

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field

from airgap_mirrors.settings.asset_policy import AssetPolicy

RepositoryName = Annotated[str, Field(pattern=r"^[A-Za-z0-9._-]+$")]


class ExternalRepoSpec(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    name: RepositoryName
    github: str = Field(pattern=r"^[A-Za-z0-9._-]+/[A-Za-z0-9._-]+$")
    assets: Annotated[AssetPolicy, BeforeValidator(AssetPolicy.from_text)] = AssetPolicy()
    asset_filter: list[str] = Field(default_factory=list)

    def wants_asset(self, file_name: str) -> bool:
        if not self.asset_filter:
            return True
        lowered: str = file_name.lower()
        return any(keyword.lower() in lowered for keyword in self.asset_filter)


class InternalRepoSpec(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    name: RepositoryName
    gitlab_path: str = Field(pattern=r"^[A-Za-z0-9._-]+(/[A-Za-z0-9._-]+)+$")
