"""Run SPM evaluation independently over rolling OOS windows."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Iterable, Sequence

from spm.backtest.aggregation import TeamOOSStats, aggregate_team_oos
from spm.backtest.market_runner import MarketBacktestObservation, run_market_backtest
from spm.backtest.windows import OOSWindow
from spm.data.models import Match
from spm.data.odds import DrawOdds


@dataclass(frozen=True, slots=True)
class WindowResult:
    window: OOSWindow
    observations: tuple[MarketBacktestObservation, ...]
    team_stats: tuple[TeamOOSStats, ...]


def run_oos_windows(
    matches: Sequence[Match],
    odds: Sequence[DrawOdds],
    windows: Sequence[OOSWindow],
    *,
    min_history: int = 3,
    threshold: float = 0.0,
    min_streak: int = 3,
    min_edge: float = 0.0,
) -> tuple[WindowResult, ...]:
    results: list[WindowResult] = []
    for window in windows:
        window_matches = [m for m in matches if window.oos_start <= m.date < window.oos_end]
        window_odds = [o for o in odds if window.oos_start <= o.date < window.oos_end]
        if not window_matches:
            continue
        observations, _ = run_market_backtest(
            window_matches,
            window_odds,
            min_history=min_history,
            threshold=threshold,
            min_streak=min_streak,
            min_edge=min_edge,
        )
        results.append(WindowResult(window, observations, aggregate_team_oos(observations)))
    return tuple(results)
