import re
from enum import StrEnum


class Platform(StrEnum):
    WINDOWS = "windows"
    LINUX = "linux"
    REDHAT = "redhat"
    AMAZON = "amazon"
    MACOS = "macos"


def _word(pattern: str) -> re.Pattern[str]:
    return re.compile(rf"(?:^|[^a-z0-9])(?:{pattern})(?:[^a-z0-9]|$)")


# Checked in this order: a RedHat package is also a Linux package, so the narrower family is tried first.
_SIGNS: list[tuple[Platform, re.Pattern[str]]] = [
    (Platform.WINDOWS, _word(r"win|win32|win64|windows|exe|msi")),
    (Platform.MACOS, _word(r"mac|macos|osx|darwin|dmg|pkg")),
    (Platform.AMAZON, _word(r"amzn\d*|amazon")),
    (Platform.REDHAT, _word(r"rpm|el\d+|rhel\d*|redhat|centos\d*|rocky\d*|alma\d*")),
    (Platform.LINUX, _word(r"linux|deb|appimage|snap|ubuntu|debian|bookworm|bullseye|buster|trixie|jammy|noble|focal")),
]


def platform_of(file_name: str) -> Platform | None:
    """The platform a release file is for, judged by its name. None means it names no platform:
    a source archive, a jar, a YAML manifest, a checksum. Those are kept whatever the platform filter."""
    lowered: str = file_name.lower()
    for platform, sign in _SIGNS:
        if sign.search(lowered):
            return platform
    return None
