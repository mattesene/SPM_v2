"""Validation and chronological ordering for imported match data."""
from __future__ import annotations

from collections import Counter
from .schema import HistoricalMatch


def validate_matches(matches: list[HistoricalMatch]) -> tuple[HistoricalMatch, ...]:
    if not matches:
        return ()
    for match in matches:
        match.validate()
    keys = [(m.match_date, m.competition, m.season, m.home_team, m.away_team) for m in matches]
    duplicates = [key for key, count in Counter(keys).items() if count > 1]
    if duplicates:
        raise ValueError(f"duplicate matches found: {duplicates[:3]}")
    return tuple(sorted(matches, key=lambda m: (m.match_date, m.competition, m.season, m.home_team, m.away_team)))
