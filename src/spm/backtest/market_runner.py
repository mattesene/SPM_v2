"""End-to-end leakage-safe backtest from historical matches to market staking."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Iterable

from spm.backtest.engine import ChronologicalBacktester
from spm.backtest.odds_staking import OddsStakingResult, simulate_draw_progression_with_odds
from spm.data.models import Match
from spm.data.odds import DrawOdds, index_draw_odds
from spm.data.normalization import canonical_team_name


@dataclass(frozen=True, slots=True)
class MarketBacktestObservation:
    date: date
    home_team: str
    away_team: str
    probability: float
    actual_draw: bool
    selected: bool
    draw_odds: float | None


def run_market_backtest(
    matches: Iterable[Match],
    odds: Iterable[DrawOdds],
    *,
    min_history: int = 3,
    threshold: float = 0.0,
    initial_bankroll: float = 1_000.0,
    base_stake: float = 10.0,
) -> tuple[tuple[MarketBacktestObservation, ...], OddsStakingResult]:
    """Run SPM chronologically, attach market prices, then stake.

    Odds are joined using the same canonical team identity used by the odds
    index, preventing formatting differences in team names from dropping a
    valid market price.
    """
    match_list = list(matches)
    odds_index = index_draw_odds(list(odds))
    backtest = ChronologicalBacktester(min_history=min_history, threshold=threshold)
    raw = backtest.run(match_list)
    observations: list[MarketBacktestObservation] = []
    selections: list[tuple[bool, float | None]] = []

    for item in raw:
        key = (
            item.date,
            canonical_team_name(item.home_team),
            canonical_team_name(item.away_team),
        )
        draw_odds = odds_index.get(key)
        observations.append(MarketBacktestObservation(
            date=item.date,
            home_team=item.home_team,
            away_team=item.away_team,
            probability=item.probability,
            actual_draw=bool(item.actual_draw),
            selected=item.selected,
            draw_odds=draw_odds,
        ))
        if item.selected:
            selections.append((bool(item.actual_draw), draw_odds))

    staking = simulate_draw_progression_with_odds(
        selections,
        initial_bankroll=initial_bankroll,
        base_stake=base_stake,
    )
    return tuple(observations), staking
