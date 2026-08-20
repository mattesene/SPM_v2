"""Aggregate walk-forward OOS staking results."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .oos_staking import OOSStakingWindowResult


@dataclass(frozen=True, slots=True)
class OOSAggregateResult:
    windows: int
    bets: int
    profit: float
    initial_bankroll: float
    final_bankroll: float
    roi: float
    max_drawdown: float
    winning_windows: int
    profitable_window_rate: float


def aggregate_oos_staking(
    results: Iterable[OOSStakingWindowResult],
    *,
    initial_bankroll: float = 1_000.0,
) -> OOSAggregateResult:
    rows = tuple(results)
    profit = sum(row.profit for row in rows)
    bets = sum(row.bets for row in rows)
    cumulative = initial_bankroll
    peak = cumulative
    max_drawdown = 0.0
    for row in rows:
        cumulative += row.profit
        peak = max(peak, cumulative)
        max_drawdown = max(max_drawdown, peak - cumulative)
    winning_windows = sum(row.profit > 0 for row in rows)
    return OOSAggregateResult(
        windows=len(rows),
        bets=bets,
        profit=profit,
        initial_bankroll=initial_bankroll,
        final_bankroll=initial_bankroll + profit,
        roi=profit / initial_bankroll if initial_bankroll else 0.0,
        max_drawdown=max_drawdown,
        winning_windows=winning_windows,
        profitable_window_rate=winning_windows / len(rows) if rows else 0.0,
    )
