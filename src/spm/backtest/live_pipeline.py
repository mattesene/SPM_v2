"""Application-level live selection pipeline."""
from __future__ import annotations

from typing import Iterable

from spm.statistics.engine import SPMScore
from .live_selection import LiveCandidate, select_live_candidates
from .oos_ranking import OOSRankingEntry


def build_live_top5(
    scores: Iterable[SPMScore],
    oos_entries: Iterable[OOSRankingEntry],
    *,
    min_bets: int = 20,
    min_profitable_window_rate: float = 0.50,
    oos_weight: float = 0.40,
) -> tuple[LiveCandidate, ...]:
    """Apply the single production selection policy used by live reports."""
    return select_live_candidates(
        scores,
        oos_entries,
        min_bets=min_bets,
        min_profitable_window_rate=min_profitable_window_rate,
        oos_weight=oos_weight,
        limit=5,
    )


def run_live_pipeline(
    scores: Iterable[SPMScore],
    oos_entries: Iterable[OOSRankingEntry],
    *,
    min_bets: int = 20,
    min_profitable_window_rate: float = 0.50,
    oos_weight: float = 0.40,
) -> tuple[LiveCandidate, ...]:
    """Public orchestration entry point for CLI/report integrations."""
    return build_live_top5(
        scores,
        oos_entries,
        min_bets=min_bets,
        min_profitable_window_rate=min_profitable_window_rate,
        oos_weight=oos_weight,
    )
