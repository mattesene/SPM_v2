"""Rank entities by out-of-sample market performance."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .oos_staking import OOSStakingWindowResult


@dataclass(frozen=True, slots=True)
class OOSRankingEntry:
    key: str
    windows: int
    bets: int
    profit: float
    roi: float
    max_drawdown: float
    profitable_window_rate: float
    score: float


def rank_oos_results(
    rows: Iterable[tuple[OOSStakingWindowResult, object]],
    *,
    key_fn,
    initial_bankroll: float = 1_000.0,
    min_bets: int = 1,
) -> tuple[OOSRankingEntry, ...]:
    """Rank by risk-adjusted OOS performance, not raw historical draw rate."""
    if initial_bankroll <= 0:
        raise ValueError("initial_bankroll must be positive")
    if min_bets < 0:
        raise ValueError("min_bets cannot be negative")
    groups: dict[str, list[OOSStakingWindowResult]] = {}
    for result, observation in rows:
        key = str(key_fn(observation))
        groups.setdefault(key, []).append(result)

    output: list[OOSRankingEntry] = []
    for key, items in groups.items():
        bets = sum(item.bets for item in items)
        if bets < min_bets:
            continue
        profit = sum(item.profit for item in items)
        roi = profit / initial_bankroll
        drawdown = max((item.max_drawdown for item in items), default=0.0)
        profitable_rate = sum(item.profit > 0 for item in items) / len(items)
        # Penalise drawdown while rewarding OOS profit and consistency.
        score = roi - (drawdown / initial_bankroll) + 0.25 * profitable_rate
        output.append(OOSRankingEntry(key, len(items), bets, profit, roi, drawdown, profitable_rate, score))
    return tuple(sorted(output, key=lambda row: (-row.score, row.key)))
