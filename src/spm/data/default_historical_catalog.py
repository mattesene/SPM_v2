"""Default historical competition/season scope used by SPM."""
from __future__ import annotations

from .historical_catalog import HistoricalCatalog, build_catalog

# Football-Data competition codes for the five major European leagues.
DEFAULT_COMPETITIONS = ("E0", "E1", "D1", "I1", "SP1")


def default_catalog(start_season: int = 1920, end_season: int = 2526) -> HistoricalCatalog:
    if start_season < 1920 or end_season < start_season:
        raise ValueError("invalid season range")
    seasons = tuple(f"{year % 100:02d}{(year + 1) % 100:02d}" for year in range(start_season, end_season))
    return build_catalog(list(DEFAULT_COMPETITIONS), list(seasons))
