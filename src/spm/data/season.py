"""In-memory season dataset and team-level aggregations."""

from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable

from .models import Match


@dataclass(frozen=True, slots=True)
class TeamStats:
    team: str
    matches: int
    goals_for: int
    goals_against: int
    draws: int

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
        stats = defaultdict(int)
        for match in self._matches:
            if match.home_team == team:
                stats["matches"] += 1
                stats["goals_for"] += match.home_goals
                stats["goals_against"] += match.away_goals
                stats["draws"] += match.is_draw
            elif match.away_team == team:
                stats["matches"] += 1
                stats["goals_for"] += match.away_goals
                stats["goals_against"] += match.home_goals
                stats["draws"] += match.is_draw
        return TeamStats(team, **stats)
