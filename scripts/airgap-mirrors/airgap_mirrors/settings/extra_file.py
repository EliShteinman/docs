from pathlib import PurePosixPath

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ExtraFile(BaseModel):
    """A file a repository needs but does not keep in git, such as a model its build downloads separately.

    `path` is where the file belongs inside the repository, so the transfer folder can be copied over a clone."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    url: str = Field(pattern=r"^https?://")
    path: str = Field(min_length=1)

    @field_validator("path")
    @classmethod
    def _inside_the_repository(cls, path: str) -> str:
        parts: list[str] = path.split("/")
        if "\\" in path or any(part in ("", ".", "..") for part in parts):
            raise ValueError(f"{path!r} must be a plain path inside the repository, like src/Resources/model.onnx")
        return path

    @property
    def file_name(self) -> str:
        return PurePosixPath(self.path).name

    @property
    def ledger_key(self) -> str:
        return f"{self.path} <- {self.url}"
