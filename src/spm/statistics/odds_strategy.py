"""OOS draw-selection and profitability bridge."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from spm.data.models import Match
from spm.data.odds import DrawOdds, index_draw_odds
from spm.data.normalization import canonical_team_name
from spm.statistics.engine import SPMEngine
from spm.statistics.profitability import BetResult, ProfitabilitySummary, summarize_bets


@dataclass(frozen=True, slots=True)
class OOSBet:
    match_date: date
    home_team: str
    away_team: str
    probability: float
    odds: float
    stake: float
    won: bool

    @property
    def edge(self) -> float:
        return self.probability * self.odds - 1.0


def run_oos_draw_strategy(
    matches: list[Match],
    odds: list[DrawOdds],
    *,
    min_probability: float = 0.0,
    min_edge: float = 0.0,
    stake: float = 1.0,
) -> tuple[tuple[OOSBet, ...], ProfitabilitySummary]:
    if stake <= 0:
        raise ValueError("stake must be positive")
    if not 0 <= min_probability <= 1:
        raise ValueError("min_probability must be in [0, 1]")

    odds_index = index_draw_odds(odds)
    ordered = sorted(matches, key=lambda match: match.date)
    engine = SPMEngine()
    bets: list[OOSBet] = []
    for match in ordered:
        key = (
            match.date,
            canonical_team_name(match.home_team),
            canonical_team_name(match.away_team),
        )
        price = odds_index.get(key)
        if price is None:
            continue
        historical = [m for m in ordered if m.date < match.date]
        score = engine.score(historical, match.home_team, match.away_team, match.date)
        if score.draw_probability < min_probability:
            continue
        if score.draw_probability * price - 1.0 < min_edge:
            continue
        bets.append(OOSBet(match.date, match.home_team, match.away_team, score.draw_probability, price, stake, match.is_draw))

    summary = summarize_bets(tuple(BetResult(b.odds, b.stake, b.won) for b in bets))
    return tuple(bets), summary
