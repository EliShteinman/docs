"""Tag every record in the NDJSON RAG feed with the docs version it belongs to.

Airgap-fork-only post-processing step. The upstream feed carries no version
metadata — the only signal is the URL path (e.g. ``/operate/rs/7.4/...``). Our
internal RAG ingests every version at once, so without an explicit tag it cannot
tell a 7.2 page from an 8.2 one. This reads ``public/docs.ndjson`` in place and
adds a ``version`` field (``"7.4"``, ``"8.2"``, or ``"latest"``) to each record
and to each of its sections, derived from the URL.

    python build/tag_ndjson_versions.py [--feed public/docs.ndjson]
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

# Products that publish versioned doc trees. A version tag is only trusted when
# the numeric segment follows one of these prefixes, so an unrelated numeric
# path segment is never mistaken for a version.
_VERSIONED_PREFIXES = (
    "operate/kubernetes",
    "operate/rs",
    "integrate/redis-data-integration",
    "develop/ai/redisvl",
)

_VERSION_PATTERN = re.compile(
    r"/(?:" + "|".join(re.escape(p) for p in _VERSIONED_PREFIXES) + r")/"
    r"(?P<version>\d+\.\d+(?:\.\d+)?)(?:/|$)"
)

LATEST = "latest"


def derive_version(url: str) -> str:
    """Return the version encoded in a page URL, or ``"latest"`` if none."""
    match = _VERSION_PATTERN.search(url)
    return match.group("version") if match else LATEST


def tag_record(record: dict[str, object]) -> str:
    """Add a ``version`` field to a record, its sections, and its child nav
    entries; return the record's version."""
    version = derive_version(str(record.get("url", "")))
    record["version"] = version
    sections = record.get("sections")
    if isinstance(sections, list):
        for section in sections:
            if isinstance(section, dict):
                section["version"] = version
    # Index-page records carry a `children[]` nav array; each child links to its
    # own page, so tag it from its own URL and fall back to the parent version.
    children = record.get("children")
    if isinstance(children, list):
        for child in children:
            if isinstance(child, dict):
                child_url = child.get("url")
                child["version"] = (
                    derive_version(str(child_url)) if child_url else version
                )
    return version


def tag_feed(feed_path: Path) -> dict[str, int]:
    """Rewrite the feed in place with version tags; return per-version counts.

    Streams line-by-line to a temp file and atomically replaces the original, so
    memory stays flat regardless of feed size and a crash mid-write cannot leave
    a truncated feed.
    """
    counts: dict[str, int] = {}
    tmp_path = feed_path.with_name(feed_path.name + ".tmp")
    with feed_path.open(encoding="utf-8") as src, tmp_path.open(
        "w", encoding="utf-8"
    ) as dst:
        for line in src:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            version = tag_record(record)
            counts[version] = counts.get(version, 0) + 1
            dst.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")))
            dst.write("\n")
    os.replace(tmp_path, feed_path)
    return counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--feed",
        type=Path,
        default=Path("public/docs.ndjson"),
        help="Path to the NDJSON feed to tag in place.",
    )
    args = parser.parse_args()

    if not args.feed.exists():
        print(f"Error: feed '{args.feed}' does not exist.", file=sys.stderr)
        return 1

    counts = tag_feed(args.feed)
    total = sum(counts.values())
    print(f"Tagged {total} records in {args.feed} with a version.")
    for version in sorted(counts):
        print(f"  {version}: {counts[version]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
