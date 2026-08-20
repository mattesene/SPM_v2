"""End-to-end SPM selection and progressive staking on chronological observations."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .market_runner import MarketBacktestObservation
from .odds_staking import OddsStakingResult, simulate_draw_progression_with_odds


@dataclass(frozen=True, slots=True)
class SPMStrategyResult:
    observations: int
    priced: int
    selected: int
    staking: OddsStakingResult


def run_spm_strategy(
    observations: Iterable[MarketBacktestObservation],
    *,
    min_edge: float = 0.0,
    min_streak: int = 0,
    initial_bankroll: float = 1_000.0,
    base_stake: float = 10.0,
) -> SPMStrategyResult:
    """Select draw opportunities using streak + edge, then stake chronologically."""
    if min_edge < 0:
        raise ValueError("min_edge cannot be negative")
    if min_streak < 0:
        raise ValueError("min_streak cannot be negative")

    rows = tuple(observations)
    selections: list[tuple[bool, float | None]] = []
    priced = selected = 0
    for row in rows:
        if row.draw_odds is None:
            continue
        priced += 1
        edge = row.probability - (1.0 / row.draw_odds)
        if row.streak >= min_streak and edge >= min_edge:
            selected += 1
            selections.append((row.actual_draw, row.draw_odds))

    staking = simulate_draw_progression_with_odds(
        selections,
        initial_bankroll=initial_bankroll,
        base_stake=base_stake,
    )
    return SPMStrategyResult(len(rows), priced, selected, staking)
