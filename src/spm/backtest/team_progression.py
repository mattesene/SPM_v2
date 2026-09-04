"""Leakage-safe historical backtest of the SPM same-team draw progression."""
from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date

from spm.data.models import Match
from spm.data.normalization import canonical_team_name
from spm.data.season import Season
from spm.statistics.engine import SPMEngine


@dataclass(frozen=True, slots=True)
class TeamProgressionObservation:
    date: date
    team: str
    opponent: str
    selected_probability: float
    streak_before: int
    actual_draw: bool
    stake_units: int


@dataclass(frozen=True, slots=True)
class TeamProgressionReport:
    observations: tuple[TeamProgressionObservation, ...]
    teams_selected: int
    series_started: int
    series_completed: int
    draws: int
    non_draws: int
    max_streak: int
    max_stake_units: int
    max_capital_units: int
    busts: int

    @property
    def bets(self) -> int:
        return len(self.observations)

    @property
    def hit_rate(self) -> float:
        return self.draws / self.bets if self.bets else 0.0

    @property
    def completion_rate(self) -> float:
        return self.series_completed / self.series_started if self.series_started else 0.0


def _team_and_opponent(match: Match, selected_team: str) -> tuple[str, str]:
    canonical = canonical_team_name(selected_team)
    if canonical_team_name(match.home_team) == canonical:
        return match.home_team, match.away_team
    return match.away_team, match.home_team


def run_team_progression_backtest(
    matches: Iterable[Match],
    *,
    min_history: int = 5,
    top_n: int = 5,
    engine: SPMEngine | None = None,
) -> TeamProgressionReport:
    """Replay live team-first selection and same-team progression chronologically.

    Every date is scored only from matches strictly before that date. New
    progressions use the top ``top_n`` distinct teams whose own historical
    sample reaches ``min_history``; an active team is then followed at its
    next fixture even if it falls out of the daily top N.
    """
    if min_history < 1 or top_n < 1:
        raise ValueError("min_history and top_n must be positive")

    ordered = sorted(matches, key=lambda m: (m.date, m.home_team, m.away_team))
    predictor = engine or SPMEngine()
    history: list[Match] = []
    active_stake: dict[str, int] = {}
    active_streak: dict[str, int] = {}
    active_probability: dict[str, float] = {}
    observations: list[TeamProgressionObservation] = []
    teams_seen: set[str] = set()
    series_started = series_completed = draws = non_draws = 0
    max_streak = max_stake = max_capital = busts = 0

    index = 0
    while index < len(ordered):
        current_date = ordered[index].date
        day_matches: list[Match] = []
        while index < len(ordered) and ordered[index].date == current_date:
            day_matches.append(ordered[index])
            index += 1

        season = Season(history)
        ready_teams = {
            canonical_team_name(team)
            for match in day_matches
            for team in (match.home_team, match.away_team)
            if season.team_stats(team).matches >= min_history
        }
        eligible_fixtures = [
            m for m in day_matches
            if canonical_team_name(m.home_team) in ready_teams
            or canonical_team_name(m.away_team) in ready_teams
        ]
        scored = predictor.rank(
            history,
            [(m.home_team, m.away_team) for m in eligible_fixtures],
            current_date,
            eligible_teams=ready_teams,
        )
        selected: dict[str, object] = {}
        for score in scored:
            team = canonical_team_name(score.selected_team)
            if team in selected:
                continue
            selected[team] = score
            if len(selected) >= top_n:
                break

        # Active progressions take precedence over a new daily selection.
        for match in day_matches:
            participants = {canonical_team_name(match.home_team), canonical_team_name(match.away_team)}
            active_today = participants.intersection(active_stake)
            new_today = participants.intersection(selected).difference(active_stake)
            teams_for_day = active_today | new_today
            for team in sorted(teams_for_day):
                if team not in active_stake:
                    score = selected[team]
                    active_stake[team] = 1
                    active_streak[team] = 0
                    active_probability[team] = float(score.team_probability)
                    series_started += 1
                    teams_seen.add(team)
                team_name, opponent = _team_and_opponent(match, team)
                stake = active_stake[team]
                streak = active_streak[team]
                is_draw = match.is_draw
                observations.append(TeamProgressionObservation(
                    current_date,
                    team_name,
                    opponent,
                    active_probability[team],
                    streak,
                    is_draw,
                    stake,
                ))
                max_stake = max(max_stake, stake)
                max_streak = max(max_streak, streak)
                if is_draw:
                    draws += 1
                    series_completed += 1
                    active_stake.pop(team, None)
                    active_streak.pop(team, None)
                    active_probability.pop(team, None)
                else:
                    non_draws += 1
                    active_stake[team] = stake * 2
                    active_streak[team] = streak + 1
                    max_capital = max(max_capital, sum(active_stake.values()))

        history.extend(day_matches)

    return TeamProgressionReport(
        tuple(observations), len(teams_seen), series_started, series_completed,
        draws, non_draws, max_streak, max_stake, max_capital, busts,
    )
