"""Historical backtest orchestration over chronologically ordered matches."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Iterable, Sequence

from .engine import BacktestEngine
from .report import BacktestReport


@dataclass(frozen=True, slots=True)
class HistoricalMatch:
    date: date
    home_team: str
    away_team: str
    home_goals: int
    away_goals: int

    @property
    def draw(self) -> int:
        return int(self.home_goals == self.away_goals)


def run_historical_backtest(
    matches: Iterable[HistoricalMatch],
    engine: BacktestEngine,
) -> BacktestReport:
    """Run a chronological backtest without exposing the current match result."""
    ordered: Sequence[HistoricalMatch] = tuple(sorted(matches, key=lambda m: m.date))
    actual: list[str] = []
    predicted: list[str] = []
    probabilities: list[float] = []
    outcomes: list[int] = []

    for match in ordered:
        prediction = engine.predict(
            home_team=match.home_team,
            away_team=match.away_team,
        )
        if prediction is not None:
            actual.append("D" if match.draw else "N")
            predicted.append("D" if prediction.selected else "N")
            probabilities.append(prediction.probability)
            outcomes.append(match.draw)
        engine.update(match.home_team, match.away_team, match.home_goals, match.away_goals)

    return BacktestReport.from_predictions(actual, predicted, probabilities, outcomes)
