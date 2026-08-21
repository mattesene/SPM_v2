"""Run chronological SPM backtests across historical CSV datasets."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from spm.data.csv import CSVMatchImporter
from spm.statistics.backtest import BacktestSummary, chronological_backtest
from spm.statistics.engine import SPMEngine


@dataclass(frozen=True, slots=True)
class DatasetBacktest:
    dataset: str
    summary: BacktestSummary


def run_dataset(path: str | Path, *, min_history: int = 1) -> DatasetBacktest:
    path = Path(path)
    matches = CSVMatchImporter().load(path)
    summary = chronological_backtest(matches, engine=SPMEngine(), min_history=min_history)
    return DatasetBacktest(path.name, summary)


def run_directory(directory: str | Path, *, min_history: int = 1) -> tuple[DatasetBacktest, ...]:
    """Backtest every CSV in a directory, in deterministic filename order."""
    directory = Path(directory)
    files = sorted(directory.glob("*.csv"))
    if not files:
        raise ValueError(f"No CSV datasets found in {directory}")
    return tuple(run_dataset(path, min_history=min_history) for path in files)
