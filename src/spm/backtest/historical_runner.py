"""Run the chronological backtester on validated historical data."""
from __future__ import annotations

from collections.abc import Iterable

from spm.backtest.engine import ChronologicalBacktester
from spm.data.normalized import MatchRecord
from spm.ingestion.backtest_input import to_backtest_matches


def run_historical_backtest(
    records: Iterable[MatchRecord],
    *,
    min_history: int = 3,
):
    """Convert validated records and execute the leakage-safe backtester."""
    matches = to_backtest_matches(records)
    return ChronologicalBacktester(min_history=min_history).run(matches)
