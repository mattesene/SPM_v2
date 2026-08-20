"""Adapt chronological OOS observations to odds-aware staking selections."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from spm.data.odds import DrawOdds
from .engine import BacktestObservation


@dataclass(frozen=True, slots=True)
class OOSOddsSelection:
    match_date: date
    home_team: str
    away_team: str
    is_draw: bool
    selected: bool
    draw_odds: float | None


def attach_odds_to_oos(
    observations: list[BacktestObservation],
    odds: list[DrawOdds],
) -> tuple[OOSOddsSelection, ...]:
    """Attach market odds to OOS observations without changing prediction logic."""
    index: dict[tuple[date, str, str], float] = {}
    for quote in odds:
        key = (quote.match_date, quote.home_team.strip().casefold(), quote.away_team.strip().casefold())
        previous = index.get(key)
        if previous is not None and previous != quote.draw_odds:
            raise ValueError(f"conflicting draw odds for {key}")
        index[key] = quote.draw_odds

    result: list[OOSOddsSelection] = []
    for observation in observations:
        key = (
            observation.date,
            observation.home_team.strip().casefold(),
            observation.away_team.strip().casefold(),
        )
        result.append(
            OOSOddsSelection(
                observation.date,
                observation.home_team,
                observation.away_team,
                bool(observation.actual_draw),
                observation.selected,
                index.get(key) if observation.selected else None,
            )
        )
    return tuple(result)
