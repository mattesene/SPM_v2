"""Reliable Top-N selection from out-of-sample SPM results."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .oos_ranking import OOSRankingEntry


@dataclass(frozen=True, slots=True)
class Top5Selection:
    entries: tuple[OOSRankingEntry, ...]
    eligible: int


def select_top5(
    entries: Iterable[OOSRankingEntry],
    *,
    min_bets: int = 20,
    min_profitable_window_rate: float = 0.50,
) -> Top5Selection:
    if min_bets < 0:
        raise ValueError("min_bets cannot be negative")
    if not 0.0 <= min_profitable_window_rate <= 1.0:
        raise ValueError("min_profitable_window_rate must be between 0 and 1")
    eligible_rows = [
        row for row in entries
        if row.bets >= min_bets
        and row.profitable_window_rate >= min_profitable_window_rate
    ]
    eligible_rows.sort(key=lambda row: (-row.score, -row.bets, row.key))
    return Top5Selection(tuple(eligible_rows[:5]), len(eligible_rows))
