"""Single entry point for generating the production live dashboard."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

from spm.statistics.engine import SPMScore
from .live_pipeline import run_live_pipeline
from .oos_ranking import OOSRankingEntry
from .live_selection import LiveCandidate
from spm.web_live import write_live_dashboard


def build_live_report(
    scores: Iterable[SPMScore],
    oos_entries: Iterable[OOSRankingEntry],
    *,
    as_of: str,
    path: str | Path,
    min_bets: int = 20,
    min_profitable_window_rate: float = 0.50,
    oos_weight: float = 0.40,
) -> tuple[LiveCandidate, ...]:
    """Select the production Top 5 and render exactly those candidates."""
    candidates = run_live_pipeline(
        scores,
        oos_entries,
        min_bets=min_bets,
        min_profitable_window_rate=min_profitable_window_rate,
        oos_weight=oos_weight,
    )
    write_live_dashboard(candidates, as_of=as_of, path=path)
    return candidates
