"""Run the historical backtest across all loaded catalog datasets."""
from __future__ import annotations

from dataclasses import dataclass

from spm.backtest.historical_batch import HistoricalBatchItem, run_historical_batch
from spm.data.normalized import MatchRecord


@dataclass(frozen=True, slots=True)
class CatalogBacktestResult:
    items: tuple[HistoricalBatchItem, ...]

    @property
    def records(self) -> int:
        return sum(item.records for item in self.items)

    @property
    def evaluated(self) -> int:
        return sum(item.evaluated for item in self.items)


def run_catalog_backtest(datasets: dict[str, list[MatchRecord]]) -> CatalogBacktestResult:
    return CatalogBacktestResult(tuple(run_historical_batch(datasets)))
