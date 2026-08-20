"""Canonical schema for historical football matches and market odds."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class HistoricalMatch:
    match_date: date
    competition: str
    season: str
    home_team: str
    away_team: str
    home_goals: int
    away_goals: int
    draw_odds: float | None = None

    @property
    def is_draw(self) -> bool:
        return self.home_goals == self.away_goals

    def validate(self) -> None:
        if not self.competition or not self.season:
            raise ValueError("competition and season are required")
        if not self.home_team or not self.away_team:
            raise ValueError("home_team and away_team are required")
        if self.home_team == self.away_team:
            raise ValueError("home_team and away_team must differ")
        if self.home_goals < 0 or self.away_goals < 0:
            raise ValueError("goals cannot be negative")
        if self.draw_odds is not None and self.draw_odds <= 1.0:
            raise ValueError("draw_odds must be greater than 1")
