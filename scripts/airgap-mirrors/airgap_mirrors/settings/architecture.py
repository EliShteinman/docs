import re
from enum import StrEnum


class Architecture(StrEnum):
    X86_64 = "x86_64"
    ARM64 = "arm64"
    ARM32 = "arm32"
    X86_32 = "x86_32"


def _word(pattern: str) -> re.Pattern[str]:
    return re.compile(rf"(?:^|[^a-z0-9])(?:{pattern})(?:[^a-z0-9]|$)")


# x86_64 is checked before x86_32 so "x86_64" is never read as plain "x86".
_SIGNS: list[tuple[Architecture, re.Pattern[str]]] = [
    (Architecture.X86_64, _word(r"x86_64|x86-64|amd64|x64|win64")),
    (Architecture.ARM64, _word(r"aarch64|arm64|armv8")),
    (Architecture.ARM32, _word(r"armhf|armel|armv7l?|armv6l?|arm")),
    (Architecture.X86_32, _word(r"i386|i686|x86|386|win32")),
]


def architecture_of(file_name: str) -> Architecture | None:
    """The processor a release file is built for, judged by its name. None means it names none:
    a Windows installer, a script, a source archive. Those are kept whatever the architecture filter."""
    lowered: str = file_name.lower()
    for architecture, sign in _SIGNS:
        if sign.search(lowered):
            return architecture
    return None
