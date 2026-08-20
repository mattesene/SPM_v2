"""Default historical dataset scope for SPM_v2 V1."""
from __future__ import annotations

from .historical_catalog import HistoricalCatalog, build_catalog

DEFAULT_COMPETITIONS = ("E0", "E1", "D1", "I1", "SP1")
DEFAULT_SEASONS = tuple(f"{year % 100:02d}{(year + 1) % 100:02d}" for year in range(19, 25))


def default_catalog() -> HistoricalCatalog:
    return build_catalog(list(DEFAULT_COMPETITIONS), list(DEFAULT_SEASONS))
