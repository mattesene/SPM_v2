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
    completed: int
    rejected: int


def run_historical_batch(paths: list[str | Path]) -> list[HistoricalBatchItem]:
    results: list[HistoricalBatchItem] = []
    for path in paths:
        records = MatchRecord.load_csv(path)
        report = run_historical_backtest(records)
        results.append(
            HistoricalBatchItem(
                str(path),
                len(records),
                report.completed,
                report.rejected,
            )
        )
    return results
