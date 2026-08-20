"""Load draw odds alongside the historical catalog."""
from __future__ import annotations

from pathlib import Path

from .historical_catalog import HistoricalCatalog
from .football_data_csv import load_football_data_odds
from .odds import DrawOdds


def load_historical_draw_odds(catalog: HistoricalCatalog, root: str | Path) -> tuple[DrawOdds, ...]:
    root = Path(root)
    odds: list[DrawOdds] = []
    for source in catalog.sources:
        path = root / source.competition / source.season / source.filename
        if not path.is_file():
            raise FileNotFoundError(path)
        odds.extend(load_football_data_odds(path))
    return tuple(sorted(odds, key=lambda item: (item.date, item.home_team, item.away_team)))
