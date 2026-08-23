"""Metrics for evaluating chronological draw predictions."""
from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from spm.backtest.engine import BacktestObservation


@dataclass(frozen=True, slots=True)
class BacktestMetrics:
    observations: int
    selected: int
    draws: int
    selected_draws: int
    selection_rate: float
    hit_rate: float
    draw_rate: float


def calculate_metrics(observations: Iterable[BacktestObservation]) -> BacktestMetrics:
    rows = tuple(observations)
    selected = tuple(row for row in rows if row.selected)
    draws = sum(row.actual_draw for row in rows)
    selected_draws = sum(row.actual_draw for row in selected)
    return BacktestMetrics(
        observations=len(rows),
        selected=len(selected),
        draws=draws,
        selected_draws=selected_draws,
        selection_rate=len(selected) / len(rows) if rows else 0.0,
        hit_rate=selected_draws / len(selected) if selected else 0.0,
        draw_rate=draws / len(rows) if rows else 0.0,
    )
