"""Source provenance attached to normalized football records."""
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True, slots=True)
class Provenance:
    source: str
    source_id: str | None = None
    source_url: str | None = None
    retrieved_at: datetime | None = None

    def __post_init__(self) -> None:
        if not self.source.strip():
            raise ValueError("source cannot be empty")

@dataclass(frozen=True, slots=True)
class SourceValue:
    value: object
    provenance: Provenance
