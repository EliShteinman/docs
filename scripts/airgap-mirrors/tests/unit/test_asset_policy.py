from datetime import UTC, date, datetime

import pytest

from airgap_mirrors.models import ReleaseRecord
from airgap_mirrors.settings import AssetPolicy, AssetPolicyKind


def release(tag: str, published: str | None) -> ReleaseRecord:
    moment: datetime | None = datetime.fromisoformat(published).replace(tzinfo=UTC) if published else None
    return ReleaseRecord(tag_name=tag, published_at=moment)


RELEASES: list[ReleaseRecord] = [
    release("v1", "2025-01-01"),
    release("v3", "2026-03-01"),
    release("v2", "2025-06-01"),
    release("undated", None),
]


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("all", AssetPolicy(kind=AssetPolicyKind.ALL)),
        ("NONE", AssetPolicy(kind=AssetPolicyKind.NONE)),
        ("latest-per-type", AssetPolicy(kind=AssetPolicyKind.LATEST_PER_TYPE)),
        ("latest:2", AssetPolicy(kind=AssetPolicyKind.LATEST, count=2)),
        ("since:2025-06-01", AssetPolicy(kind=AssetPolicyKind.SINCE, since=date(2025, 6, 1))),
    ],
)
def test_policy_text_is_parsed(text: str, expected: AssetPolicy) -> None:
    assert AssetPolicy.from_text(text) == expected


@pytest.mark.parametrize("text", ["some", "latest:", "latest:x", "since:2025-1-1", "latest:0"])
def test_bad_policy_text_is_refused(text: str) -> None:
    with pytest.raises(ValueError, match=r"policy|greater"):
        AssetPolicy.from_text(text)


def test_non_text_passes_through_to_validation() -> None:
    assert AssetPolicy.from_text({"kind": "none"}) == {"kind": "none"}


@pytest.mark.parametrize(
    ("policy", "expected_tags"),
    [
        ("all", ["v1", "v3", "v2", "undated"]),
        ("none", []),
        ("latest:2", ["v3", "v2"]),
        ("since:2025-06-01", ["v3", "v2"]),
    ],
)
def test_policy_selects_releases(policy: str, expected_tags: list[str]) -> None:
    chosen: AssetPolicy = AssetPolicy.from_text(policy)  # type: ignore[assignment]
    assert [item.tag_name for item in chosen.select(RELEASES)] == expected_tags


def preview(tag: str, published: str, *, flagged: bool = True) -> ReleaseRecord:
    return ReleaseRecord(
        tag_name=tag, prerelease=flagged, published_at=datetime.fromisoformat(published).replace(tzinfo=UTC)
    )


PER_TYPE: AssetPolicy = AssetPolicy(kind=AssetPolicyKind.LATEST_PER_TYPE)


def test_per_type_takes_the_newest_stable_and_a_newer_preview() -> None:
    releases: list[ReleaseRecord] = [*RELEASES, preview("8.12-rc3", "2026-04-01"), preview("8.12-rc2", "2026-03-15")]
    assert [item.tag_name for item in PER_TYPE.select(releases)] == ["v3", "8.12-rc3"]


def test_per_type_drops_a_preview_older_than_the_stable_release() -> None:
    releases: list[ReleaseRecord] = [*RELEASES, preview("v3-rc1", "2026-02-01")]
    assert [item.tag_name for item in PER_TYPE.select(releases)] == ["v3"]


def test_per_type_takes_the_preview_alone_when_nothing_is_stable() -> None:
    assert [item.tag_name for item in PER_TYPE.select([preview("1.0-beta1", "2026-01-01")])] == ["1.0-beta1"]


@pytest.mark.parametrize(
    ("tag", "expected"),
    [
        ("8.12-rc3", True),
        ("2.0.0-beta1", True),
        ("6.2.0.M1", True),
        ("v1.0.0-alpha", True),
        ("7.2.4", False),
        ("6.1.7.RELEASE", False),
        ("v0.95.2", False),
    ],
)
def test_preview_is_recognised_by_its_tag(tag: str, expected: bool) -> None:
    assert preview(tag, "2026-01-01", flagged=False).is_prerelease is expected
