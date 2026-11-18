from pydantic import BaseModel, ConfigDict, Field

from airgap_mirrors.models.repository_state import RepositoryState


class ExportLedger(BaseModel):
    """Online side: the state the last export sent. Nothing comes back from the air-gapped side, so what was
    sent is taken as delivered, and the next export carries only what came after it."""

    model_config = ConfigDict(frozen=True)

    sent: RepositoryState | None = None

    def with_sent(self, state: RepositoryState) -> "ExportLedger":
        return self.model_copy(update={"sent": state})


class SentAssets(BaseModel):
    """Online side: the release files already sent, as "<tag>/<file name>", so no export sends one twice."""

    model_config = ConfigDict(frozen=True)

    files: set[str] = Field(default_factory=set)

    def with_file(self, key: str) -> "SentAssets":
        return self.model_copy(update={"files": self.files | {key}})


class ImportLedger(BaseModel):
    """Air-gapped side: the transfers already applied to the local copy."""

    model_config = ConfigDict(frozen=True)

    applied_state_ids: list[str] = Field(default_factory=list)

    def with_applied(self, state_id: str) -> "ImportLedger":
        if state_id in self.applied_state_ids:
            return self
        return self.model_copy(update={"applied_state_ids": [*self.applied_state_ids, state_id]})
