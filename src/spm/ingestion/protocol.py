"""Provider-neutral ingestion contracts."""
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from spm.data.normalized import MatchRecord


@dataclass(frozen=True, slots=True)
class FetchBatch:
    source: str
    retrieved_at: datetime
    records: tuple[MatchRecord, ...]


class MatchSourceAdapter(Protocol):
    source_name: str

    def fetch(self, **kwargs) -> FetchBatch:
        """Fetch data using a provider-permitted access mechanism."""
        ...
