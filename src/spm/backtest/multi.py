"""Aggregate backtest execution across competition/season slices."""
from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from spm.backtest.dataset import group_by_competition_season
from spm.backtest.runner import BacktestSlice, run_slice
from spm.data.normalized import MatchRecord


@dataclass(frozen=True, slots=True)
class MultiBacktestReport:
    slices: tuple[BacktestSlice, ...]

    @property
    def total_samples(self) -> int:
        return sum(item.report.samples for item in self.slices)

    @property
    def total_correct(self) -> int:
        return sum(item.report.correct for item in self.slices)

    @property
    def accuracy(self) -> float:
        return self.total_correct / self.total_samples if self.total_samples else 0.0


def run_multi(
    records: Iterable[MatchRecord],
    min_history: int = 1,
    threshold: float = 0.0,
) -> MultiBacktestReport:
    """Run isolated chronological backtests for every competition/season slice."""
    slices = [
        run_slice(list(group), min_history=min_history, threshold=threshold)
        for group in group_by_competition_season(records).values()
    ]
    slices.sort(key=lambda item: (item.competition, item.season))
    return MultiBacktestReport(tuple(slices))
