"""Canonical records used by the multi-source ingestion layer."""

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class SourceRef:
    source: str
    source_id: str | None = None
    source_url: str | None = None


@dataclass(frozen=True, slots=True)
class MatchRecord:
    date: date
    competition: str
    season: str
    home_team: str
    away_team: str
    home_goals: int | None
    away_goals: int | None
    source: SourceRef

    @property
    def is_finished(self) -> bool:
        return self.home_goals is not None and self.away_goals is not None
