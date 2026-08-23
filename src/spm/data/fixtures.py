"""Persistence model for upcoming fixtures used by the live pipeline."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class Fixture:
    date: date
    home_team: str
    away_team: str
    competition: str | None = None

    def __post_init__(self) -> None:
        if not self.home_team.strip() or not self.away_team.strip():
            raise ValueError("Team names cannot be empty")
        if self.home_team.strip().casefold() == self.away_team.strip().casefold():
            raise ValueError("Home and away teams must be different")
