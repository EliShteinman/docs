import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

_PRERELEASE_TAG = re.compile(r"(?:^|[.\-_])(?:rc|beta|alpha|preview|m)\d*(?:[.\-_]|$)", re.IGNORECASE)


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

    @property
    def is_prerelease(self) -> bool:
        """Marked as a pre-release on GitHub, or named like one (8.12-rc3, 2.0.0-beta1, 6.2.0.M1)."""
        return self.prerelease or bool(_PRERELEASE_TAG.search(self.tag_name))


class ReleaseCatalog(BaseModel):
    model_config = ConfigDict(frozen=True)

    repository: str
    releases: list[ReleaseRecord] = Field(default_factory=list)
