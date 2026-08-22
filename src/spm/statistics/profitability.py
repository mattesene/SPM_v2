"""Out-of-sample profitability calculations for draw selections."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BetResult:
    odds: float
    stake: float
    won: bool

    @property
    def profit(self) -> float:
        return self.stake * (self.odds - 1.0) if self.won else -self.stake


@dataclass(frozen=True, slots=True)
class ProfitabilitySummary:
    bets: int
    wins: int
    stake: float
    profit: float

    @property
    def roi(self) -> float:
        return self.profit / self.stake if self.stake else 0.0


def summarize_bets(results: tuple[BetResult, ...]) -> ProfitabilitySummary:
    return ProfitabilitySummary(
        bets=len(results),
        wins=sum(result.won for result in results),
        stake=sum(result.stake for result in results),
        profit=sum(result.profit for result in results),
    )
