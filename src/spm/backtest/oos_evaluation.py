"""Out-of-sample evaluation helpers for SPM market selections."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .market_runner import MarketBacktestObservation


@dataclass(frozen=True, slots=True)
class OOSMetrics:
    observations: int
    priced: int
    selected: int
    draws: int
    selected_draws: int
    selection_rate: float
    selected_draw_rate: float
    mean_edge: float
    positive_edge_rate: float


def evaluate_oos(
    observations: Iterable[MarketBacktestObservation],
    *,
    min_edge: float = 0.0,
) -> OOSMetrics:
    if min_edge < 0.0:
        raise ValueError("min_edge cannot be negative")
    rows = tuple(observations)
    priced = [row for row in rows if row.draw_odds is not None]
    selected = [
        row for row in priced
        if row.probability - (1.0 / row.draw_odds) >= min_edge
    ]
    edges = [row.probability - (1.0 / row.draw_odds) for row in priced]
    positive = sum(edge > 0.0 for edge in edges)
    return OOSMetrics(
        observations=len(rows),
        priced=len(priced),
        selected=len(selected),
        draws=sum(row.actual_draw for row in rows),
        selected_draws=sum(row.actual_draw for row in selected),
        selection_rate=len(selected) / len(priced) if priced else 0.0,
        selected_draw_rate=sum(row.actual_draw for row in selected) / len(selected) if selected else 0.0,
        mean_edge=sum(edges) / len(edges) if edges else 0.0,
        positive_edge_rate=positive / len(edges) if edges else 0.0,
    )
