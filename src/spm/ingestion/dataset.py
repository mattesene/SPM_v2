"""Build a chronologically ordered historical match dataset."""
from __future__ import annotations

from collections.abc import Iterable

from spm.data.normalized import MatchRecord
from spm.ingestion.historical import COMPETITIONS, fetch_seasons


def build_historical_dataset(
    seasons: Iterable[str],
    competitions: Iterable[str] = COMPETITIONS,
) -> tuple[MatchRecord, ...]:
    """Load historical slices and return one deterministic chronological dataset."""
    records = fetch_seasons(seasons, competitions)
    return tuple(sorted(records, key=lambda match: (match.date, match.competition, match.home_team, match.away_team)))
