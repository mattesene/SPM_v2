"""Draw probability and betting edge calculations."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DrawEdge:
    probability: float
    odds: float
    implied_probability: float
    edge: float


def calculate_draw_edge(probability: float, odds: float) -> DrawEdge:
    if not 0.0 <= probability <= 1.0:
        raise ValueError("probability must be between 0 and 1")
    if odds <= 1.0:
        raise ValueError("odds must be greater than 1")
    implied = 1.0 / odds
    return DrawEdge(probability, odds, implied, probability - implied)
