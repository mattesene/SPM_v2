"""Chronological backtesting for the SPM draw model."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from spm.data.models import Match
from spm.statistics.engine import SPMEngine


@dataclass(frozen=True, slots=True)
class BacktestResult:
    date: date
    home_team: str
    away_team: str
    draw_probability: float
    actual_draw: int
    brier_score: float


@dataclass(frozen=True, slots=True)
class BacktestSummary:
    results: tuple[BacktestResult, ...]
    skipped: int

    @property
    def evaluated(self) -> int:
        return len(self.results)

    @property
    def brier_score(self) -> float:
        if not self.results:
            return 0.0
        return sum(item.brier_score for item in self.results) / len(self.results)

    @property
    def actual_draw_rate(self) -> float:
        if not self.results:
            return 0.0
        return sum(item.actual_draw for item in self.results) / len(self.results)


def chronological_backtest(
    matches: list[Match],
    *,
    engine: SPMEngine | None = None,
    min_history: int = 1,
) -> BacktestSummary:
    """Evaluate every match using only matches strictly before its date.

    Matches for which either team has fewer than ``min_history`` previous
    appearances are skipped. This prevents look-ahead leakage and makes the
    initial warm-up period explicit.
    """
    if min_history < 1:
        raise ValueError("min_history must be positive")

    ordered = sorted(matches, key=lambda item: (item.date, item.home_team, item.away_team))
    engine = engine or SPMEngine()
    history: list[Match] = []
    results: list[BacktestResult] = []
    skipped = 0

    for match in ordered:
        home_history = sum(1 for item in history if match.home_team in (item.home_team, item.away_team))
        away_history = sum(1 for item in history if match.away_team in (item.home_team, item.away_team))
        if home_history < min_history or away_history < min_history:
            skipped += 1
            history.append(match)
            continue

        score = engine.score(history, match.home_team, match.away_team, match.date)
        actual_draw = int(match.is_draw)
        results.append(
            BacktestResult(
                match.date,
                match.home_team,
                match.away_team,
                score.draw_probability,
                actual_draw,
                (score.draw_probability - actual_draw) ** 2,
            )
        )
        history.append(match)

    return BacktestSummary(tuple(results), skipped)
