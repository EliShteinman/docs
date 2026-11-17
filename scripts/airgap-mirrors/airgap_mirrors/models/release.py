from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ReleaseAsset(BaseModel):
    model_config = ConfigDict(extra="ignore", frozen=True, populate_by_name=True)

    name: str = Field(min_length=1)
    size: int = Field(ge=0)
    download_url: str = Field(alias="browser_download_url")


class ReleaseRecord(BaseModel):
    model_config = ConfigDict(extra="ignore", frozen=True)

    tag_name: str = Field(min_length=1)
    name: str | None = None
    body: str | None = None
    published_at: datetime | None = None
    draft: bool = False
    prerelease: bool = False
    assets: list[ReleaseAsset] = Field(default_factory=list)

    @property
    def title(self) -> str:
        return self.name or self.tag_name


class ReleaseCatalog(BaseModel):
    model_config = ConfigDict(frozen=True)

    repository: str
    releases: list[ReleaseRecord] = Field(default_factory=list)
