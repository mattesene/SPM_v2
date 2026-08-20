"""Build chronological team draw streak features without future leakage."""
from __future__ import annotations

from dataclasses import dataclass
from collections import defaultdict
from .schema import HistoricalMatch


@dataclass(frozen=True, slots=True)
class TeamMatchFeature:
    match: HistoricalMatch
    team: str
    draw_streak_before: int


def build_team_features(matches: tuple[HistoricalMatch, ...]) -> tuple[TeamMatchFeature, ...]:
    """Emit one feature row per team-match using only matches strictly before it."""
    streak: dict[str, int] = defaultdict(int)
    rows: list[TeamMatchFeature] = []
    for match in matches:
        for team in (match.home_team, match.away_team):
            rows.append(TeamMatchFeature(match, team, streak[team]))
        if match.is_draw:
            streak[match.home_team] = 0
            streak[match.away_team] = 0
        else:
            streak[match.home_team] += 1
            streak[match.away_team] += 1
    return tuple(rows)
