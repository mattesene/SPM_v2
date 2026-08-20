"""Leakage-safe conversion of model/market edge into staking selections."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .market_runner import MarketBacktestObservation
from .odds_staking import OddsStakingResult, simulate_draw_progression_with_odds


@dataclass(frozen=True, slots=True)
class EdgeStakingResult:
    observations: int
    priced: int
    selected: int
    positive_edge: int
    staking: OddsStakingResult


def run_edge_staking(
    observations: Iterable[MarketBacktestObservation],
    *,
    min_edge: float = 0.0,
    initial_bankroll: float = 1_000.0,
    base_stake: float = 10.0,
) -> EdgeStakingResult:
    """Stake only when model probability exceeds market implied probability."""
    if min_edge < 0.0:
        raise ValueError("min_edge cannot be negative")
    rows = tuple(observations)
    selections: list[tuple[bool, float | None]] = []
    priced = positive_edge = selected = 0
    for row in rows:
        if row.draw_odds is None:
            continue
        priced += 1
        edge = row.probability - (1.0 / row.draw_odds)
        if edge >= min_edge:
            selected += 1
            positive_edge += int(edge > 0.0)
            selections.append((row.actual_draw, row.draw_odds))
    staking = simulate_draw_progression_with_odds(
        selections,
        initial_bankroll=initial_bankroll,
        base_stake=base_stake,
    )
    return EdgeStakingResult(len(rows), priced, selected, positive_edge, staking)
