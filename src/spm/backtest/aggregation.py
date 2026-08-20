"""Aggregation helpers for OOS SPM backtests."""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable

from .market_runner import MarketBacktestObservation


@dataclass(frozen=True, slots=True)
class TeamOOSStats:
    team: str
    observations: int
    selections: int
    draws: int
    hit_rate: float


def aggregate_team_oos(observations: Iterable[MarketBacktestObservation]) -> tuple[TeamOOSStats, ...]:
    data: dict[str, list[int]] = defaultdict(lambda: [0, 0, 0])
    for row in observations:
        for team in (row.home_team, row.away_team):
            data[team][0] += 1
        if row.selected:
            # The match is a single betting opportunity, attributed to both participating teams.
            for team in (row.home_team, row.away_team):
                data[team][1] += 1
                data[team][2] += int(row.actual_draw)
    result = []
    for team, (observations_count, selections, draws) in data.items():
        result.append(TeamOOSStats(
            team=team,
            observations=observations_count,
            selections=selections,
            draws=draws,
            hit_rate=(draws / selections) if selections else 0.0,
        ))
    return tuple(sorted(result, key=lambda x: (-x.hit_rate, -x.selections, x.team)))
