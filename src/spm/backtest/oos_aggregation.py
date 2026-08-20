"""Aggregate rolling OOS observations using the actual observation schema."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .window_runner import WindowResult


@dataclass(frozen=True, slots=True)
class OOSAggregate:
    windows: int
    observations: int
    selected: int
    draws: int
    hit_rate: float


def aggregate_oos_results(results: Iterable[WindowResult]) -> OOSAggregate:
    items = tuple(results)
    observations = tuple(row for item in items for row in item.observations)
    selected = tuple(row for row in observations if row.selected)
    draws = sum(int(row.actual_draw) for row in selected)
    return OOSAggregate(
        windows=len(items),
        observations=len(observations),
        selected=len(selected),
        draws=draws,
        hit_rate=(draws / len(selected)) if selected else 0.0,
    )
