import re
from datetime import UTC, date, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator

from airgap_mirrors.models.release import ReleaseRecord

_LATEST = re.compile(r"^latest:(\d+)$")
_SINCE = re.compile(r"^since:(\d{4}-\d{2}-\d{2})$")
_OLDEST = datetime.min.replace(tzinfo=UTC)


class AssetPolicyKind(StrEnum):
    ALL = "all"
    NONE = "none"
    LATEST = "latest"
    SINCE = "since"


class AssetPolicy(BaseModel):
    """Which releases get their files downloaded. Release notes are always copied."""

    model_config = ConfigDict(frozen=True)

    kind: AssetPolicyKind = AssetPolicyKind.ALL
    count: int | None = Field(default=None, ge=1)
    since: date | None = None

    @model_validator(mode="after")
    def _has_its_parameter(self) -> "AssetPolicy":
        if self.kind is AssetPolicyKind.LATEST and self.count is None:
            raise ValueError("latest needs a count: latest:N")
        if self.kind is AssetPolicyKind.SINCE and self.since is None:
            raise ValueError("since needs a date: since:YYYY-MM-DD")
        return self

    @classmethod
    def from_text(cls, value: object) -> object:
        if not isinstance(value, str):
            return value
        text: str = value.strip().lower()
        if text in (AssetPolicyKind.ALL, AssetPolicyKind.NONE):
            return cls(kind=AssetPolicyKind(text))
        if latest := _LATEST.match(text):
            return cls(kind=AssetPolicyKind.LATEST, count=int(latest.group(1)))
        if since := _SINCE.match(text):
            return cls(kind=AssetPolicyKind.SINCE, since=date.fromisoformat(since.group(1)))
        raise ValueError(f"unknown asset policy {value!r}: use all, none, latest:N or since:YYYY-MM-DD")

    def select(self, releases: list[ReleaseRecord]) -> list[ReleaseRecord]:
        if self.kind is AssetPolicyKind.ALL:
            return list(releases)
        if self.kind is AssetPolicyKind.NONE:
            return []
        if self.kind is AssetPolicyKind.LATEST:
            newest_first: list[ReleaseRecord] = sorted(releases, key=_published, reverse=True)
            return newest_first[: self.count]
        return [release for release in releases if release.published_at and release.published_at.date() >= self.since]


def _published(release: ReleaseRecord) -> datetime:
    return release.published_at or _OLDEST
