"""Walk-forward evaluation of model-to-market edge thresholds."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .market_runner import MarketBacktestObservation
from .oos_evaluation import OOSMetrics, evaluate_oos


@dataclass(frozen=True, slots=True)
class EdgeWalkForwardWindow:
    train_start: int
    train_end: int
    test_start: int
    test_end: int
    threshold: float
    train_metrics: OOSMetrics
    test_metrics: OOSMetrics


def run_edge_walk_forward(
    observations: Iterable[MarketBacktestObservation],
    thresholds: Iterable[float],
    *,
    train_size: int,
    test_size: int,
) -> tuple[EdgeWalkForwardWindow, ...]:
    """Select edge threshold on each train window and evaluate only next test window.

    The threshold is selected using training mean edge, then the selected
    threshold is evaluated on the immediately following observations. No test
    result participates in threshold selection.
    """
    rows = tuple(observations)
    candidates = tuple(sorted(set(thresholds)))
    if not candidates or any(value < 0.0 for value in candidates):
        raise ValueError("thresholds must contain non-negative values")
    if train_size <= 0 or test_size <= 0:
        raise ValueError("train_size and test_size must be positive")

    windows: list[EdgeWalkForwardWindow] = []
    start = 0
    while start + train_size + test_size <= len(rows):
        train = rows[start:start + train_size]
        test = rows[start + train_size:start + train_size + test_size]
        ranked = []
        for threshold in candidates:
            metrics = evaluate_oos(train, min_edge=threshold)
            # Prefer higher realized selected draw rate, then more selections,
            # then lower threshold for deterministic tie-breaking.
            ranked.append((metrics.selected_draw_rate, metrics.selected, -threshold, threshold, metrics))
        _, _, _, selected_threshold, train_metrics = max(ranked)
        test_metrics = evaluate_oos(test, min_edge=selected_threshold)
        windows.append(EdgeWalkForwardWindow(
            train_start=start,
            train_end=start + train_size,
            test_start=start + train_size,
            test_end=start + train_size + test_size,
            threshold=selected_threshold,
            train_metrics=train_metrics,
            test_metrics=test_metrics,
        ))
        start += test_size
    return tuple(windows)
