"""Application-level policy for selecting the live Top 5."""
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
    """Apply the production policy and always return at most five live picks."""
    return select_live_candidates(
        scores,
        oos_entries,
        min_bets=min_bets,
        min_profitable_window_rate=min_profitable_window_rate,
        oos_weight=oos_weight,
        limit=5,
    )
