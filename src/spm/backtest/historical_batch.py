"""Batch execution helpers for historical SPM datasets."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from spm.backtest.historical_runner import run_historical_backtest
from spm.data.normalized import MatchRecord


@dataclass(frozen=True, slots=True)
class HistoricalBatchItem:
    path: str
    records: int
    evaluated: int
    not_evaluated: int


def run_historical_batch(
    records_by_source: dict[str | Path, list[MatchRecord]],
    *,
    min_history: int = 3,
) -> list[HistoricalBatchItem]:
    """Run independent normalized datasets and summarize evaluated observations."""
    results: list[HistoricalBatchItem] = []
    for path, records in records_by_source.items():
        observations = run_historical_backtest(records, min_history=min_history)
        evaluated = len(observations)
        results.append(
            HistoricalBatchItem(
                str(path),
                len(records),
                evaluated,
                len(records) - evaluated,
            )
        )
    return results
