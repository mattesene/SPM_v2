"""High-level pipeline for running historical backtests from normalized data."""
from __future__ import annotations

from collections.abc import Callable, Iterable

from spm.backtest.engine import ChronologicalBacktester
from spm.backtest.multi import MultiBacktestReport, run_multi
from spm.data.normalized import MatchRecord


def run_historical_pipeline(
    records: Iterable[MatchRecord],
    engine_factory: Callable[[], ChronologicalBacktester],
) -> MultiBacktestReport:
    """Run normalized records through isolated chronological backtests."""
    materialized = tuple(records)
    if not materialized:
        raise ValueError("records cannot be empty")
    return run_multi(materialized, engine_factory)
