"""Aggregate backtest execution across competition/season slices."""
from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Iterable

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


def run_multi(records: Iterable[MatchRecord], engine_factory) -> MultiBacktestReport:
    """Run isolated backtests, creating a fresh engine for every slice."""
    slices: list[BacktestSlice] = []
    for group in group_by_competition_season(records).values():
        slices.append(run_slice(list(group), engine_factory()))
    slices.sort(key=lambda item: (item.competition, item.season))
    return MultiBacktestReport(tuple(slices))
