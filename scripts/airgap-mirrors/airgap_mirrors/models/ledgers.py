from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from airgap_mirrors.models.repository_state import RepositoryState


class ExportLedger(BaseModel):
    """Online side: the state GitLab is known to have, and states sent but not yet confirmed."""

    model_config = ConfigDict(frozen=True)

    confirmed: RepositoryState | None = None
    pending: dict[str, RepositoryState] = Field(default_factory=dict)

    def with_pending(self, state: RepositoryState) -> "ExportLedger":
        return self.model_copy(update={"pending": {**self.pending, state.state_id: state}})

    def with_confirmed(self, state_id: str) -> "ExportLedger":
        remaining: dict[str, RepositoryState] = {key: value for key, value in self.pending.items() if key != state_id}
        return self.model_copy(update={"confirmed": self.pending[state_id], "pending": remaining})


class ImportLedger(BaseModel):
    """Air-gapped side: the transfers already applied to the local copy."""

    model_config = ConfigDict(frozen=True)

    applied_state_ids: list[str] = Field(default_factory=list)

    def with_applied(self, state_id: str) -> "ImportLedger":
        if state_id in self.applied_state_ids:
            return self
        return self.model_copy(update={"applied_state_ids": [*self.applied_state_ids, state_id]})


class ImportedState(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    state_id: str


class ImportReceipt(BaseModel):
    """Carried back to the online side: which states now live in GitLab, in the order they were applied."""

    model_config = ConfigDict(frozen=True)

    imported_at: datetime
    entries: list[ImportedState] = Field(default_factory=list)
