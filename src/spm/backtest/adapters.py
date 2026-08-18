"""Adapters from normalized ingestion records to backtest matches."""
from __future__ import annotations

from collections.abc import Iterable

from spm.data.models import Match
from spm.data.normalized import MatchRecord


def completed_matches(records: Iterable[MatchRecord]) -> tuple[Match, ...]:
    """Convert completed normalized records into the backtest domain model."""
    matches: list[Match] = []
    for record in records:
        if not record.completed:
            continue
        matches.append(
            Match(
                date=record.date,
                home_team=record.canonical_home_team,
                away_team=record.canonical_away_team,
                home_goals=record.home_goals,  # type: ignore[arg-type]
                away_goals=record.away_goals,  # type: ignore[arg-type]
            )
        )
    return tuple(matches)
