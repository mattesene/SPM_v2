"""Flatten and chronologically order the historical catalog datasets."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

from .historical_catalog import HistoricalCatalog
from .historical_loader import load_catalog
from .normalized import MatchRecord


def load_historical_records(catalog: HistoricalCatalog, root: str | Path) -> tuple[MatchRecord, ...]:
    datasets = load_catalog(catalog, root)
    records: list[MatchRecord] = []
    for rows in datasets.values():
        records.extend(rows)
    return tuple(sorted(records, key=lambda row: (row.date, row.competition or "", row.season or "", row.home_team, row.away_team)))
