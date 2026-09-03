"""In-memory season dataset and team-level aggregations."""

from dataclasses import dataclass
from typing import Iterable

from .models import Match
from .normalization import canonical_team_name


@dataclass(frozen=True, slots=True)
class TeamStats:
    team: str
    matches: int = 0
    goals_for: int = 0
    goals_against: int = 0
    draws: int = 0

    @property
    def goals_for_avg(self) -> float:
        return self.goals_for / self.matches if self.matches else 0.0

    @property
    def goals_against_avg(self) -> float:
        return self.goals_against / self.matches if self.matches else 0.0

    @property
    def draw_rate(self) -> float:
        return self.draws / self.matches if self.matches else 0.0


class Season:
    """Collection of matches with deterministic team aggregations."""

    def __init__(self, matches: Iterable[Match] = ()) -> None:
        self._matches = list(matches)

    @property
    def matches(self) -> tuple[Match, ...]:
        return tuple(self._matches)

    def add(self, match: Match) -> None:
        self._matches.append(match)

    def team_stats(self, team: str) -> TeamStats:
        canonical = canonical_team_name(team)
        matches = goals_for = goals_against = draws = 0
        for match in self._matches:
            home = canonical_team_name(match.home_team)
            away = canonical_team_name(match.away_team)
            if home == canonical:
                matches += 1
                goals_for += match.home_goals
                goals_against += match.away_goals
                draws += match.is_draw
            elif away == canonical:
                matches += 1
                goals_for += match.away_goals
                goals_against += match.home_goals
                draws += match.is_draw
        return TeamStats(canonical, matches, goals_for, goals_against, draws)
