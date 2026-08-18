"""Run reproducible historical backtests by competition and season."""
from __future__ import annotations

from dataclasses import dataclass

from spm.backtest.adapters import completed_matches
from spm.backtest.historical import run_historical_backtest
from spm.backtest.report import BacktestReport
from spm.data.normalized import MatchRecord


@dataclass(frozen=True, slots=True)
class BacktestSlice:
    competition: str
    season: str
    report: BacktestReport


def run_slice(
    records: list[MatchRecord],
    min_history: int = 1,
    threshold: float = 0.0,
) -> BacktestSlice:
    """Run one competition/season slice from normalized records."""
    if not records:
        raise ValueError("records cannot be empty")
    competition = records[0].competition or "unknown"
    season = records[0].season or "unknown"
    if any((r.competition or "unknown") != competition or (r.season or "unknown") != season for r in records):
        raise ValueError("records must belong to one competition and season")
    report = run_historical_backtest(
        list(completed_matches(records)),
        min_history=min_history,
        threshold=threshold,
    )
    return BacktestSlice(competition, season, report)
