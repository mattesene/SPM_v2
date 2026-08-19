"""Threshold sensitivity analysis without selecting a winner automatically."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .market_runner import MarketBacktestObservation


@dataclass(frozen=True, slots=True)
class ThresholdResult:
    threshold: float
    observations: int
    selected: int
    priced_selected: int
    draws_selected: int
    priced_draw_rate: float
    selection_rate: float


def evaluate_thresholds(
    observations: Iterable[MarketBacktestObservation],
    thresholds: Iterable[float],
) -> tuple[ThresholdResult, ...]:
    """Describe threshold sensitivity on already generated out-of-sample scores.

    This function deliberately does not choose the best threshold. Threshold
    selection must happen on a training/calibration window and be frozen before
    the corresponding test window is evaluated.
    """
    rows = tuple(observations)
    results: list[ThresholdResult] = []
    for threshold in thresholds:
        if not 0.0 <= threshold <= 1.0:
            raise ValueError("threshold must be between 0 and 1")
        selected = [row for row in rows if row.probability >= threshold]
        priced = [row for row in selected if row.draw_odds is not None]
        draws = sum(row.actual_draw for row in priced)
        results.append(
            ThresholdResult(
                threshold=threshold,
                observations=len(rows),
                selected=len(selected),
                priced_selected=len(priced),
                draws_selected=draws,
                priced_draw_rate=draws / len(priced) if priced else 0.0,
                selection_rate=len(selected) / len(rows) if rows else 0.0,
            )
        )
    return tuple(results)
