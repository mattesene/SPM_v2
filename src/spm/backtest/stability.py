"""Stability metrics for SPM OOS team rankings across evaluation windows."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from .ranking import RankedTeam, rank_teams
from .aggregation import TeamOOSStats


@dataclass(frozen=True, slots=True)
class TeamStability:
    team: str
    windows_present: int
    mean_lower_bound: float
    mean_hit_rate: float
    mean_selections: float
    stability_score: float


def rank_stability(windows: Sequence[Iterable[TeamOOSStats]], *, min_selections: int = 20, top_n: int = 5) -> tuple[TeamStability, ...]:
    if not windows:
        return ()
    per_team: dict[str, list[RankedTeam]] = {}
    for stats in windows:
        for ranked in rank_teams(stats, min_selections=min_selections, top_n=max(top_n, 20)):
            per_team.setdefault(ranked.team, []).append(ranked)
    result: list[TeamStability] = []
    total_windows = len(windows)
    for team, rows in per_team.items():
        present = len(rows)
        mean_lb = sum(r.lower_bound for r in rows) / present
        mean_hr = sum(r.hit_rate for r in rows) / present
        mean_sel = sum(r.selections for r in rows) / present
        stability = (present / total_windows) * mean_lb
        result.append(TeamStability(team, present, mean_lb, mean_hr, mean_sel, stability))
    return tuple(sorted(result, key=lambda x: (-x.stability_score, -x.windows_present, -x.mean_selections, x.team))[:top_n])
