"""High-level pipeline for running historical backtests from normalized data."""
from __future__ import annotations

from collections.abc import Iterable

from spm.backtest.multi import MultiBacktestReport, run_multi
from spm.data.normalized import MatchRecord


def run_historical_pipeline(
    records: Iterable[MatchRecord],
    min_history: int = 1,
    threshold: float = 0.0,
) -> MultiBacktestReport:
    """Run normalized records through isolated chronological backtests."""
    materialized = tuple(records)
    if not materialized:
        raise ValueError("records cannot be empty")
    return run_multi(materialized, min_history=min_history, threshold=threshold)
