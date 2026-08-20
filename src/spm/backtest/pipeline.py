"""High-level historical and rolling OOS backtest pipelines."""
from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Sequence

from spm.backtest.final_ranking import FinalRankedTeam, final_top_teams
from spm.backtest.multi import MultiBacktestReport, run_multi
from spm.backtest.window_runner import WindowResult, run_oos_windows
from spm.backtest.windows import OOSWindow
from spm.data.models import Match
from spm.data.normalized import MatchRecord
from spm.data.odds import DrawOdds


@dataclass(frozen=True, slots=True)
class OOSPipelineResult:
    windows: tuple[WindowResult, ...]
    ranking: tuple[FinalRankedTeam, ...]


def run_historical_pipeline(
    records: Iterable[MatchRecord],
    min_history: int = 1,
    threshold: float = 0.0,
) -> MultiBacktestReport:
    """Run normalized records through isolated chronological backtests."""
    materialized = tuple(records)
    if not materialized:
        raise ValueError("records cannot be empty")
    return run_multi(materialized, min_history=min_history, threshold=threshold)


def evaluate_rolling_oos(
    matches: Sequence[Match],
    odds: Sequence[DrawOdds],
    windows: Sequence[OOSWindow],
    *,
    min_history: int = 3,
    threshold: float = 0.0,
    min_streak: int = 3,
    min_edge: float = 0.0,
    min_selections: int = 20,
    top_n: int = 5,
) -> OOSPipelineResult:
    """Run independent OOS windows and produce a stability-ranked Top N."""
    results = run_oos_windows(
        matches, odds, windows,
        min_history=min_history,
        threshold=threshold,
        min_streak=min_streak,
        min_edge=min_edge,
    )
    ranking = final_top_teams(
        [item.team_stats for item in results],
        min_selections=min_selections,
        top_n=top_n,
    )
    return OOSPipelineResult(results, ranking)
