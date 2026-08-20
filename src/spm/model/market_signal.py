"""Market-aware SPM signal selection."""
from __future__ import annotations

from dataclasses import dataclass
from .draw_edge import DrawEdge, calculate_draw_edge


@dataclass(frozen=True, slots=True)
class MarketSignal:
    team: str
    streak: int
    edge: DrawEdge
    selected: bool


def build_market_signal(
    team: str,
    streak: int,
    probability: float,
    draw_odds: float | None,
    *,
    min_streak: int = 0,
    min_edge: float = 0.0,
) -> MarketSignal:
    if not team:
        raise ValueError("team is required")
    if streak < 0 or min_streak < 0:
        raise ValueError("streak cannot be negative")
    if draw_odds is None:
        raise ValueError("draw odds are required for a market signal")
    edge = calculate_draw_edge(probability, draw_odds)
    return MarketSignal(team, streak, edge, streak >= min_streak and edge.edge >= min_edge)
