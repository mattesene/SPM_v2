"""Reliability-aware OOS ranking for SPM teams."""
from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Iterable

from .aggregation import TeamOOSStats


@dataclass(frozen=True, slots=True)
class RankedTeam:
    team: str
    selections: int
    hit_rate: float
    lower_bound: float
    score: float


def wilson_lower_bound(hits: int, trials: int, z: float = 1.96) -> float:
    if trials <= 0 or hits < 0 or hits > trials:
        raise ValueError("invalid hit/trial counts")
    p = hits / trials
    denominator = 1 + z * z / trials
    centre = p + z * z / (2 * trials)
    margin = z * sqrt(p * (1 - p) / trials + z * z / (4 * trials * trials))
    return (centre - margin) / denominator


def rank_teams(stats: Iterable[TeamOOSStats], *, min_selections: int = 20, top_n: int = 5) -> tuple[RankedTeam, ...]:
    if min_selections < 1 or top_n < 1:
        raise ValueError("min_selections and top_n must be positive")
    ranked = []
    for item in stats:
        if item.selections < min_selections:
            continue
        lower = wilson_lower_bound(item.draws, item.selections)
        ranked.append(RankedTeam(item.team, item.selections, item.hit_rate, lower, lower))
    return tuple(sorted(ranked, key=lambda x: (-x.score, -x.selections, x.team))[:top_n])
