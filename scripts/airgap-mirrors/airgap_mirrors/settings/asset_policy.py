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
    LATEST_PER_TYPE = "latest-per-type"
    SINCE = "since"


class AssetPolicy(BaseModel):
    """Which releases get their files downloaded. Release notes are always copied.

    latest-per-type works per release line (the tag before its version, so redisctl and redisctl-mcp are
    two lines) and, within a line, per type: the newest stable release and a newer pre-release."""

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
        if text in (AssetPolicyKind.ALL, AssetPolicyKind.NONE, AssetPolicyKind.LATEST_PER_TYPE):
            return cls(kind=AssetPolicyKind(text))
        if latest := _LATEST.match(text):
            return cls(kind=AssetPolicyKind.LATEST, count=int(latest.group(1)))
        if since := _SINCE.match(text):
            return cls(kind=AssetPolicyKind.SINCE, since=date.fromisoformat(since.group(1)))
        raise ValueError(
            f"unknown asset policy {value!r}: use all, none, latest-per-type, latest:N or since:YYYY-MM-DD"
        )

    def select(self, releases: list[ReleaseRecord]) -> list[ReleaseRecord]:
        if self.kind is AssetPolicyKind.ALL:
            return list(releases)
        if self.kind is AssetPolicyKind.NONE:
            return []
        if self.kind is AssetPolicyKind.LATEST_PER_TYPE:
            return [chosen for line in _by_line(releases) for chosen in _newest_stable_and_newer_prerelease(line)]
        if self.kind is AssetPolicyKind.LATEST:
            newest_first: list[ReleaseRecord] = sorted(releases, key=_published, reverse=True)
            return newest_first[: self.count]
        return [release for release in releases if release.published_at and release.published_at.date() >= self.since]


def _published(release: ReleaseRecord) -> datetime:
    return release.published_at or _OLDEST


def _newest_stable_and_newer_prerelease(releases: list[ReleaseRecord]) -> list[ReleaseRecord]:
    """The newest stable release, plus the newest pre-release when it is newer than that stable one.
    An older pre-release has already turned into a stable release, so its files are not needed."""
    stable: list[ReleaseRecord] = [release for release in releases if not release.is_prerelease]
    previews: list[ReleaseRecord] = [release for release in releases if release.is_prerelease]
    newest_stable: ReleaseRecord | None = max(stable, key=_published, default=None)
    newest_preview: ReleaseRecord | None = max(previews, key=_published, default=None)
    chosen: list[ReleaseRecord] = [newest_stable] if newest_stable else []
    if newest_preview and (newest_stable is None or _published(newest_preview) > _published(newest_stable)):
        chosen.append(newest_preview)
    return chosen


def _by_line(releases: list[ReleaseRecord]) -> list[list[ReleaseRecord]]:
    lines: dict[str, list[ReleaseRecord]] = {}
    for release in releases:
        lines.setdefault(release.release_line, []).append(release)
    return list(lines.values())
