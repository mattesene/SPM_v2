"""Historical Football-Data ingestion helpers."""
from __future__ import annotations

from collections.abc import Iterable

from spm.data.normalized import MatchRecord
from spm.ingestion.football_data import FootballDataAdapter

COMPETITIONS = ("E0", "E1", "E2", "E3", "I1", "I2", "SP1", "SP2", "D1", "D2", "F1", "F2")


def fetch_seasons(
    seasons: Iterable[str],
    competitions: Iterable[str] = COMPETITIONS,
    adapter: FootballDataAdapter | None = None,
) -> tuple[MatchRecord, ...]:
    """Fetch and flatten public CSV slices for the requested seasons."""
    adapter = adapter or FootballDataAdapter()
    records: list[MatchRecord] = []
    for season in seasons:
        for competition in competitions:
            records.extend(adapter.fetch(season=season, competition=competition).records)
    return tuple(records)
