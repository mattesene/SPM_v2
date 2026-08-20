"""Final SPM ranking built from repeated OOS windows."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from .aggregation import TeamOOSStats
from .stability import TeamStability, rank_stability


@dataclass(frozen=True, slots=True)
class FinalRankedTeam:
    rank: int
    team: str
    windows_present: int
    mean_lower_bound: float
    mean_hit_rate: float
    mean_selections: float
    stability_score: float


def final_top_teams(
    windows: Sequence[Iterable[TeamOOSStats]],
    *,
    min_selections: int = 20,
    top_n: int = 5,
) -> tuple[FinalRankedTeam, ...]:
    stability: tuple[TeamStability, ...] = rank_stability(
        windows, min_selections=min_selections, top_n=top_n
    )
    return tuple(
        FinalRankedTeam(
            rank=index,
            team=item.team,
            windows_present=item.windows_present,
            mean_lower_bound=item.mean_lower_bound,
            mean_hit_rate=item.mean_hit_rate,
            mean_selections=item.mean_selections,
            stability_score=item.stability_score,
        )
        for index, item in enumerate(stability, start=1)
    )
