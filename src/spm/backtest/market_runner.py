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
from spm.model.market_signal import build_market_signal


@dataclass(frozen=True, slots=True)
class MarketBacktestObservation:
    date: date
    home_team: str
    away_team: str
    probability: float
    actual_draw: bool
    selected: bool
    selected_team: str | None
    draw_odds: float | None
    home_streak: int = 0
    away_streak: int = 0


def run_market_backtest(
    matches: Iterable[Match],
    odds: Iterable[DrawOdds],
    *,
    min_history: int = 3,
    threshold: float = 0.0,
    min_streak: int = 0,
    min_edge: float = 0.0,
    initial_bankroll: float = 1_000.0,
    base_stake: float = 10.0,
) -> tuple[tuple[MarketBacktestObservation, ...], OddsStakingResult]:
    """Run SPM chronologically using only pre-match information."""
    match_list = list(matches)
    odds_index = index_draw_odds(list(odds))
    backtest = ChronologicalBacktester(min_history=min_history, threshold=threshold)
    raw = backtest.run(match_list)
    observations: list[MarketBacktestObservation] = []
    selections: list[tuple[bool, float | None]] = []
    streaks: dict[str, int] = {}

    for item in raw:
        home = canonical_team_name(item.home_team)
        away = canonical_team_name(item.away_team)
        draw_odds = odds_index.get((item.date, home, away))
        home_streak = streaks.get(home, 0)
        away_streak = streaks.get(away, 0)
        selected_team: str | None = None
        if draw_odds is not None:
            signal_home = build_market_signal(home, home_streak, item.probability, draw_odds,
                                              min_streak=min_streak, min_edge=min_edge)
            signal_away = build_market_signal(away, away_streak, item.probability, draw_odds,
                                              min_streak=min_streak, min_edge=min_edge)
            if signal_home.selected:
                selected_team = home
            elif signal_away.selected:
                selected_team = away
        selected = selected_team is not None
        observations.append(MarketBacktestObservation(
            date=item.date, home_team=item.home_team, away_team=item.away_team,
            probability=item.probability, actual_draw=bool(item.actual_draw),
            selected=selected, selected_team=selected_team, draw_odds=draw_odds,
            home_streak=home_streak, away_streak=away_streak,
        ))
        if item.selected and draw_odds is None:
            selections.append((bool(item.actual_draw), None))
        elif selected:
            selections.append((bool(item.actual_draw), draw_odds))
        if item.actual_draw:
            streaks[home] = 0
            streaks[away] = 0
        else:
            streaks[home] = home_streak + 1
            streaks[away] = away_streak + 1

    staking = simulate_draw_progression_with_odds(
        selections, initial_bankroll=initial_bankroll, base_stake=base_stake,
    )
    return tuple(observations), staking
