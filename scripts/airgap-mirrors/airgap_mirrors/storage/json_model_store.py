import logging
import os
import tempfile
from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel, ValidationError

from airgap_mirrors.exceptions import TransferError

ModelT = TypeVar("ModelT", bound=BaseModel)

logger: logging.Logger = logging.getLogger(__name__)


class JsonModelStore:
    """Saves models as JSON. A write goes to a temporary file first, so a crash never leaves half a file."""

    def load(self, path: Path, model_type: type[ModelT]) -> ModelT | None:
        if not path.exists():
            return None
        try:
            return model_type.model_validate_json(path.read_text(encoding="utf-8"))
        except ValidationError as invalid:
            raise TransferError(f"{path} is damaged or from another tool version: {invalid}") from invalid

    def save(self, path: Path, model: BaseModel) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temporary = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.")
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(model.model_dump_json(indent=2, by_alias=True))
        os.replace(temporary, path)
        logger.debug("saved %s", path)
