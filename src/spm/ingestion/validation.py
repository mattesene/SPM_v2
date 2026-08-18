"""Validation and cleanup helpers for historical match datasets."""
from __future__ import annotations

from collections.abc import Iterable

from spm.data.normalized import MatchRecord


def validate_historical_dataset(records: Iterable[MatchRecord]) -> tuple[MatchRecord, ...]:
    """Return completed, de-duplicated records in deterministic chronological order."""
    unique: dict[tuple, MatchRecord] = {}
    for record in records:
        if not record.completed:
            continue
        key = (
            record.date,
            record.competition,
            record.season,
            record.canonical_home_team,
            record.canonical_away_team,
        )
        unique[key] = record
    return tuple(sorted(unique.values(), key=lambda r: (r.date, r.competition, r.season, r.canonical_home_team, r.canonical_away_team)))
