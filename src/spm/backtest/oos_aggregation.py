"""Aggregate rolling OOS economic results without pooling away window boundaries."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .window_runner import WindowResult


@dataclass(frozen=True, slots=True)
class OOSAggregate:
    windows: int
    observations: int
    selected: int
    wins: int
    bets: int
    profit: float
    final_bankroll_sum: float
    max_drawdown: float
    max_exposure: float

    @property
    def hit_rate(self) -> float:
        return self.wins / self.bets if self.bets else 0.0

    @property
    def roi(self) -> float:
        return self.profit / self._capital_basis if self._capital_basis else 0.0

    @property
    def _capital_basis(self) -> float:
        # Each window is independently evaluated from the same default bankroll.
        return float(self.windows * 1_000.0)


def aggregate_oos_results(results: Iterable[WindowResult]) -> OOSAggregate:
    items = tuple(results)
    bets = sum(item.team_stats[0].bets if item.team_stats else 0 for item in items)
    wins = sum(item.team_stats[0].wins if item.team_stats else 0 for item in items)
    selected = sum(1 for item in items for observation in item.observations if observation.selected)
    observations = sum(len(item.observations) for item in items)
    profit = 0.0
    final_sum = 0.0
    max_dd = 0.0
    max_exposure = 0.0
    for item in items:
        # team_stats contains economic aggregates; when absent, the window is empty.
        for stat in item.team_stats:
            profit += stat.profit
            final_sum += stat.final_bankroll
            max_dd = max(max_dd, stat.max_drawdown)
            max_exposure = max(max_exposure, stat.max_exposure)
    return OOSAggregate(len(items), observations, selected, wins, bets, profit, final_sum, max_dd, max_exposure)
