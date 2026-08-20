"""Run the chronological backtester on validated historical data."""
from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from spm.backtest.engine import ChronologicalBacktester
from spm.data.default_historical_catalog import default_catalog
from spm.data.historical_ingest import ingest_catalog
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


def run_default_catalog_backtest(root: str | Path, *, min_history: int = 3):
    """Ingest the complete V1 catalog and run the leakage-safe backtest."""
    ingestion = ingest_catalog(default_catalog(), root)
    records = [record for dataset in ingestion.datasets.values() for record in dataset]
    return run_historical_backtest(records, min_history=min_history)
