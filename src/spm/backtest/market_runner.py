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
    draw_odds: float | None = None
    home_streak: int = 0
    away_streak: int = 0
    selected_team: str | None = None


def _streaks_before_matches(matches: list[Match]) -> dict[Match, tuple[int, int]]:
    """Return each fixture's team non-draw streak immediately before kickoff."""
    streaks: dict[str, int] = {}
    result: dict[Match, tuple[int, int]] = {}
    for match in sorted(matches, key=lambda item: (item.date, item.home_team, item.away_team)):
        home = canonical_team_name(match.home_team)
        away = canonical_team_name(match.away_team)
        home_streak = streaks.get(home, 0)
        away_streak = streaks.get(away, 0)
        result[match] = (home_streak, away_streak)
        if match.is_draw:
            streaks[home] = 0
            streaks[away] = 0
        else:
            streaks[home] = home_streak + 1
            streaks[away] = away_streak + 1
    return result


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
    """Run SPM chronologically using only pre-match information.

    Streaks are computed from every prior match, including the warm-up period
    before the statistical model has enough history to emit a prediction.
    When both teams qualify, the stronger market edge wins; streak is the
    deterministic tie-breaker.
    """
    match_list = list(matches)
    odds_index = index_draw_odds(list(odds))
    streaks_before = _streaks_before_matches(match_list)
    backtest = ChronologicalBacktester(min_history=min_history, threshold=threshold)
    raw = backtest.run(match_list)
    observations: list[MarketBacktestObservation] = []
    selections: list[tuple[str, bool, float | None]] = []

    by_identity: dict[tuple[date, str, str], list[Match]] = {}
    for match in match_list:
        key = (match.date, canonical_team_name(match.home_team), canonical_team_name(match.away_team))
        by_identity.setdefault(key, []).append(match)

    for item in raw:
        home = canonical_team_name(item.home_team)
        away = canonical_team_name(item.away_team)
        draw_odds = odds_index.get((item.date, home, away))
        candidates = by_identity[(item.date, home, away)]
        if len(candidates) != 1:
            raise ValueError(f"ambiguous canonical fixture identity: {(item.date, home, away)}")
        source_match = candidates[0]
        home_streak, away_streak = streaks_before[source_match]
        selected_team: str | None = None

        if draw_odds is not None:
            signals = (
                build_market_signal(
                    home, home_streak, item.probability, draw_odds,
                    min_streak=min_streak, min_edge=min_edge,
                ),
                build_market_signal(
                    away, away_streak, item.probability, draw_odds,
                    min_streak=min_streak, min_edge=min_edge,
                ),
            )
            qualifying = [signal for signal in signals if signal.selected]
            if qualifying:
                best = max(qualifying, key=lambda signal: (signal.edge.edge, signal.streak, signal.team))
                selected_team = best.team

        selected = selected_team is not None
        observations.append(MarketBacktestObservation(
            date=item.date,
            home_team=item.home_team,
            away_team=item.away_team,
            probability=item.probability,
            actual_draw=bool(item.actual_draw),
            selected=selected,
            draw_odds=draw_odds,
            home_streak=home_streak,
            away_streak=away_streak,
            selected_team=selected_team,
        ))

        if selected and draw_odds is not None:
            selections.append((selected_team, bool(item.actual_draw), draw_odds))

    staking = simulate_draw_progression_with_odds(
        selections,
        initial_bankroll=initial_bankroll,
        base_stake=base_stake,
    )
    return tuple(observations), staking
