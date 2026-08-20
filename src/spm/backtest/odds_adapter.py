"""Adapt chronological OOS observations to odds-aware staking selections."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from spm.data.odds import DrawOdds
from spm.data.models import Match
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
    index = {
        (q.match_date, q.home_team.strip().casefold(), q.away_team.strip().casefold()): q.draw_odds
        for q in odds
    }
    result: list[OOSOddsSelection] = []
    for observation in observations:
        match: Match = observation.match
        key = (match.date, match.home_team.strip().casefold(), match.away_team.strip().casefold())
        result.append(OOSOddsSelection(
            match.date, match.home_team, match.away_team,
            observation.actual_draw, observation.selected, index.get(key) if observation.selected else None,
        ))
    return tuple(result)
