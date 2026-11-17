from typing import Protocol, TypeVar

from airgap_mirrors.exceptions import ConfigurationError


class NamedSpec(Protocol):
    @property
    def name(self) -> str: ...


SpecT = TypeVar("SpecT", bound=NamedSpec)


def require_unique_names(specs: list[SpecT]) -> list[SpecT]:
    seen: set[str] = set()
    for spec in specs:
        if spec.name in seen:
            raise ValueError(f"repository {spec.name!r} is listed twice")
        seen.add(spec.name)
    return specs


def pick(specs: list[SpecT], wanted: list[str]) -> list[SpecT]:
    if not wanted:
        return list(specs)
    known: set[str] = {spec.name for spec in specs}
    unknown: list[str] = [name for name in wanted if name not in known]
    if unknown:
        raise ConfigurationError(f"not in the config: {', '.join(unknown)}")
    return [spec for spec in specs if spec.name in wanted]
