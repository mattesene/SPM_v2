"""Canonical normalized match record used by all data sources."""
from dataclasses import dataclass
from datetime import date

from .normalization import canonical_team_name
from .provenance import Provenance


@dataclass(frozen=True, slots=True)
class MatchRecord:
    date: date
    home_team: str
    away_team: str
    home_goals: int | None = None
    away_goals: int | None = None
    competition: str | None = None
    season: str | None = None
    provenance: tuple[Provenance, ...] = ()

    def __post_init__(self) -> None:
        if not self.home_team.strip() or not self.away_team.strip():
            raise ValueError("team names cannot be empty")
        if self.home_goals is not None and self.home_goals < 0:
            raise ValueError("home_goals cannot be negative")
        if self.away_goals is not None and self.away_goals < 0:
            raise ValueError("away_goals cannot be negative")

    @property
    def canonical_home_team(self) -> str:
        return canonical_team_name(self.home_team)

    @property
    def canonical_away_team(self) -> str:
        return canonical_team_name(self.away_team)

    @property
    def completed(self) -> bool:
        return self.home_goals is not None and self.away_goals is not None

    @property
    def source_count(self) -> int:
        return len(self.provenance)

    @property
    def identity_key(self) -> tuple[date, str, str, str | None]:
        return (self.date, self.canonical_home_team, self.canonical_away_team, self.competition)
