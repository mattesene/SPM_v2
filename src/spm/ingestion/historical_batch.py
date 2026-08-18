"""Batch historical data ingestion helpers."""
from __future__ import annotations

from collections.abc import Iterable

from spm.data.normalized import MatchRecord
from spm.ingestion.football_data import load_season


def load_historical_batch(
    competitions: Iterable[str],
    seasons: Iterable[str],
) -> list[MatchRecord]:
    """Load all requested competition/season slices into one normalized dataset."""
    records: list[MatchRecord] = []
    for competition in competitions:
        for season in seasons:
            records.extend(load_season(competition, season))
    return sorted(records, key=lambda record: (record.competition, record.season, record.date, record.home_team, record.away_team))
