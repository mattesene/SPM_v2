"""Chronological, leakage-safe backtesting for the SPM draw model."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from spm.data.models import Match
from spm.data.season import Season
from spm.statistics.model import PareggioModel


@dataclass(frozen=True, slots=True)
class BacktestObservation:
    date: object
    home_team: str
    away_team: str
    probability: float
    actual_draw: int
    selected: bool


class ChronologicalBacktester:
    """Evaluate each match using only matches that occurred before it."""

    def __init__(self, model: PareggioModel | None = None, min_history: int = 1, threshold: float = 0.0) -> None:
        if min_history < 1:
            raise ValueError("min_history must be positive")
        if not 0.0 <= threshold <= 1.0:
            raise ValueError("threshold must be between 0 and 1")
        self.model = model or PareggioModel()
        self.min_history = min_history
        self.threshold = threshold

    def run(self, matches: Iterable[Match]) -> tuple[BacktestObservation, ...]:
        ordered = sorted(matches, key=lambda match: (match.date, match.home_team, match.away_team))
        history = Season()
        observations: list[BacktestObservation] = []
        for match in ordered:
            home_stats = history.team_stats(match.home_team)
            away_stats = history.team_stats(match.away_team)
            if home_stats.matches >= self.min_history and away_stats.matches >= self.min_history:
                prediction = self.model.predict(history, match.home_team, match.away_team)
                observations.append(
                    BacktestObservation(
                        match.date,
                        match.home_team,
                        match.away_team,
                        prediction.probability,
                        int(match.is_draw),
                        prediction.probability >= self.threshold,
                    )
                )
            history.add(match)
        return tuple(observations)
