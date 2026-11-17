from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from airgap_mirrors.models.repository_state import RepositoryState


class TransferManifest(BaseModel):
    """Travels next to a bundle: which repository it belongs to and what the repository must look like after it."""

    model_config = ConfigDict(frozen=True)

    format_version: Literal[1] = 1
    name: str = Field(min_length=1)
    upstream_url: str
    state: RepositoryState
    base_state_id: str | None = None
    bundle_file: str | None = None
    created_at: datetime
