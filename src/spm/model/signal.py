"""SPM draw-betting signal construction."""
from __future__ import annotations

from dataclasses import dataclass

from .draw_edge import DrawEdge, calculate_draw_edge


@dataclass(frozen=True, slots=True)
class SPMSignal:
    team: str
    draw_streak: int
    edge: DrawEdge
    selected: bool


def build_signal(
    team: str,
    draw_streak: int,
    probability: float,
    draw_odds: float,
    *,
    min_streak: int = 0,
    min_edge: float = 0.0,
) -> SPMSignal:
    if not team:
        raise ValueError("team is required")
    if draw_streak < 0 or min_streak < 0:
        raise ValueError("streak values cannot be negative")
    edge = calculate_draw_edge(probability, draw_odds)
    selected = draw_streak >= min_streak and edge.edge >= min_edge
    return SPMSignal(team, draw_streak, edge, selected)
