import hashlib
import json

from pydantic import BaseModel, ConfigDict, Field


class RepositoryState(BaseModel):
    """What a repository looks like at one moment: its default branch and every branch and tag tip."""

    model_config = ConfigDict(frozen=True)

    default_branch: str = Field(min_length=1)
    refs: dict[str, str] = Field(default_factory=dict)

    @property
    def state_id(self) -> str:
        canonical: str = json.dumps({"default_branch": self.default_branch, "refs": self.refs}, sort_keys=True)
        return hashlib.sha256(canonical.encode()).hexdigest()

    def object_ids(self) -> set[str]:
        return set(self.refs.values())

    def refs_changed_since(self, base: "RepositoryState | None") -> list[str]:
        base_refs: dict[str, str] = base.refs if base else {}
        return sorted(name for name, object_id in self.refs.items() if base_refs.get(name) != object_id)
