"""Metrics for evaluating the draw-selection rule."""
from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Iterable

from spm.backtest.engine import BacktestObservation


@dataclass(frozen=True, slots=True)
class SelectionMetrics:
    observations: int
    selected: int
    draws: int
    selected_draws: int
    draw_rate: float
    selected_draw_rate: float


def summarize_selection(observations: Iterable[BacktestObservation]) -> SelectionMetrics:
    rows = tuple(observations)
    selected = tuple(row for row in rows if row.selected)
    draws = sum(row.actual_draw for row in rows)
    selected_draws = sum(row.actual_draw for row in selected)
    return SelectionMetrics(
        observations=len(rows),
        selected=len(selected),
        draws=draws,
        selected_draws=selected_draws,
        draw_rate=draws / len(rows) if rows else 0.0,
        selected_draw_rate=selected_draws / len(selected) if selected else 0.0,
    )
