"""Compact, deterministic summary of out-of-sample ranking results."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .oos_ranking import OOSRankingEntry


@dataclass(frozen=True, slots=True)
class OOSSummary:
    entities: int
    eligible_entities: int
    total_bets: int
    total_profit: float
    average_roi: float
    best_key: str | None


def summarize_oos(entries: Iterable[OOSRankingEntry], *, min_bets: int = 1) -> OOSSummary:
    rows = tuple(entries)
    if min_bets < 0:
        raise ValueError("min_bets cannot be negative")
    eligible = tuple(row for row in rows if row.bets >= min_bets)
    total_bets = sum(row.bets for row in eligible)
    total_profit = sum(row.profit for row in eligible)
    average_roi = sum(row.roi for row in eligible) / len(eligible) if eligible else 0.0
    best_key = eligible[0].key if eligible else None
    return OOSSummary(len(rows), len(eligible), total_bets, total_profit, average_roi, best_key)
