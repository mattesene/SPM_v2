"""Market edge calculations for out-of-sample SPM selections."""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Iterable

from .market_runner import MarketBacktestObservation


@dataclass(frozen=True, slots=True)
class EdgeObservation:
    probability: float
    draw_odds: float
    implied_probability: float
    edge: float
    selected: bool


def calculate_edge(probability: float, draw_odds: float) -> float:
    if not 0.0 <= probability <= 1.0:
        raise ValueError("probability must be between 0 and 1")
    if draw_odds <= 1.0 or not isfinite(draw_odds):
        raise ValueError("draw_odds must be finite and greater than 1")
    return probability - (1.0 / draw_odds)


def evaluate_market_edge(
    observations: Iterable[MarketBacktestObservation],
    *,
    min_edge: float = 0.0,
) -> tuple[EdgeObservation, ...]:
    if min_edge < 0.0:
        raise ValueError("min_edge cannot be negative")
    results: list[EdgeObservation] = []
    for row in observations:
        if row.draw_odds is None:
            continue
        implied = 1.0 / row.draw_odds
        edge = calculate_edge(row.probability, row.draw_odds)
        results.append(EdgeObservation(
            probability=row.probability,
            draw_odds=row.draw_odds,
            implied_probability=implied,
            edge=edge,
            selected=edge >= min_edge,
        ))
    return tuple(results)
