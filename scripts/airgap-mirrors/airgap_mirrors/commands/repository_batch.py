import logging
from collections.abc import Callable, Sequence
from typing import Protocol, TypeVar

from airgap_mirrors.exceptions import AirgapMirrorError

logger: logging.Logger = logging.getLogger(__name__)


class Named(Protocol):
    @property
    def name(self) -> str: ...


SpecT = TypeVar("SpecT", bound=Named)


class RepositoryBatch:
    """Runs one step for every repository. A failure in one repository is reported and the rest still run."""

    def run(self, step_name: str, specs: Sequence[SpecT], step: Callable[[SpecT], object]) -> list[str]:
        failed: list[str] = []
        for spec in specs:
            try:
                step(spec)
            except AirgapMirrorError as failure:
                logger.error("%s: %s failed: %s", spec.name, step_name, failure)
                failed.append(spec.name)
        return failed
