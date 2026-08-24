"""Aggregate historical SPM backtest results."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from spm.statistics.backtest_runner import DatasetBacktest, run_directory


@dataclass(frozen=True, slots=True)
class AggregateResult:
    datasets: tuple[DatasetBacktest, ...]

    @property
    def evaluated(self) -> int:
        return sum(item.summary.evaluated for item in self.datasets)

    @property
    def skipped(self) -> int:
        return sum(item.summary.skipped for item in self.datasets)

    @property
    def brier_score(self) -> float:
        evaluated = self.evaluated
        if not evaluated:
            return 0.0
        return sum(item.summary.brier_score * item.summary.evaluated for item in self.datasets) / evaluated

    @property
    def actual_draw_rate(self) -> float:
        evaluated = self.evaluated
        if not evaluated:
            return 0.0
        return sum(item.summary.actual_draw_rate * item.summary.evaluated for item in self.datasets) / evaluated


def aggregate_directory(directory: str | Path, *, min_history: int = 1) -> AggregateResult:
    """Run and aggregate all CSV datasets in ``directory``."""
    return AggregateResult(run_directory(directory, min_history=min_history))


def csv_rows(report: AggregateResult) -> list[str]:
    rows = ["dataset,evaluated,skipped,brier_score,actual_draw_rate"]
    for item in report.datasets:
        rows.append(
            f"{item.dataset},{item.summary.evaluated},{item.summary.skipped},"
            f"{item.summary.brier_score:.6f},{item.summary.actual_draw_rate:.6f}"
        )
    rows.append(
        f"TOTAL,{report.evaluated},{report.skipped},{report.brier_score:.6f},{report.actual_draw_rate:.6f}"
    )
    return rows
