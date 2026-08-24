"""Adapt chronological OOS observations to odds-aware staking selections."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from spm.data.normalization import canonical_team_name
from spm.data.odds import DrawOdds, index_draw_odds
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
    index_draw_odds(odds)
    index = {q.identity_key: q.draw_odds for q in odds}
    result: list[OOSOddsSelection] = []
    for observation in observations:
        key = (
            observation.date,
            canonical_team_name(observation.home_team),
            canonical_team_name(observation.away_team),
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
