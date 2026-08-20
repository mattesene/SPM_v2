"""Conversion from normalized historical records to the backtest Match model."""
from __future__ import annotations

from collections.abc import Iterable

from .models import Match
from .normalized import MatchRecord


def to_completed_matches(records: Iterable[MatchRecord]) -> tuple[Match, ...]:
    """Keep only completed matches and fail loudly on invalid historical rows."""
    matches: list[Match] = []
    for record in records:
        if not record.completed:
            continue
        matches.append(Match(
            date=record.date,
            home_team=record.canonical_home_team,
            away_team=record.canonical_away_team,
            home_goals=record.home_goals,  # type: ignore[arg-type]
            away_goals=record.away_goals,  # type: ignore[arg-type]
        ))
    return tuple(sorted(matches, key=lambda match: (match.date, match.home_team, match.away_team)))
