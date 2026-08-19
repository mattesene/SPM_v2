"""Market draw-odds records used for odds-aware backtesting."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from .normalization import canonical_team_name


@dataclass(frozen=True, slots=True)
class DrawOdds:
    date: date
    home_team: str
    away_team: str
    draw_odds: float

    def __post_init__(self) -> None:
        if not self.home_team.strip() or not self.away_team.strip():
            raise ValueError("team names cannot be empty")
        if self.draw_odds <= 1.0:
            raise ValueError("draw_odds must be greater than 1.0")

    @property
    def identity_key(self) -> tuple[date, str, str]:
        return (
            self.date,
            canonical_team_name(self.home_team),
            canonical_team_name(self.away_team),
        )


def index_draw_odds(records: list[DrawOdds]) -> dict[tuple[date, str, str], float]:
    """Index odds and reject conflicting duplicate match prices."""
    indexed: dict[tuple[date, str, str], float] = {}
    for record in records:
        key = record.identity_key
        previous = indexed.get(key)
        if previous is not None and previous != record.draw_odds:
            raise ValueError(f"conflicting draw odds for {key}")
        indexed[key] = record.draw_odds
    return indexed
