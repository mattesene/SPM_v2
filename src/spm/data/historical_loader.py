"""Load cached historical CSV files through the existing football-data provider."""
from __future__ import annotations

from pathlib import Path

from .historical_catalog import HistoricalCatalog
from .providers.football_data import FootballDataProvider


def load_catalog(catalog: HistoricalCatalog, root: str | Path):
    root = Path(root)
    provider = FootballDataProvider()
    datasets = {}
    for source in catalog.sources:
        path = root / source.competition / source.season / source.filename
        if not path.exists():
            raise FileNotFoundError(path)
        datasets[(source.competition, source.season)] = provider.load(path)
    return datasets
