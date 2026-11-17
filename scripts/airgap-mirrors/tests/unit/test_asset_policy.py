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
