"""Combine OOS ranking metrics with statistical stability diagnostics."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .oos_ranking import OOSRankingEntry
from .statistical_stability import StabilityMetrics, binomial_stability


@dataclass(frozen=True, slots=True)
class StableRankingEntry:
    ranking: OOSRankingEntry
    stability: StabilityMetrics
    robust: bool


def add_stability(
    entries: Iterable[OOSRankingEntry],
    *,
    min_lower_95: float = 0.0,
) -> tuple[StableRankingEntry, ...]:
    if not 0.0 <= min_lower_95 <= 1.0:
        raise ValueError("min_lower_95 must be between 0 and 1")
    result = []
    for entry in entries:
        trials = entry.bets
        successes = round(entry.profitable_window_rate * entry.windows)
        stability = binomial_stability(successes, entry.windows) if entry.windows else binomial_stability(0, 1)
        robust = stability.lower_95 >= min_lower_95
        result.append(StableRankingEntry(entry, stability, robust))
    return tuple(result)
