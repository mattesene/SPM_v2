"""Catalog of historical competition/season sources."""
from __future__ import annotations

from dataclasses import dataclass

from .season_urls import SeasonSource, football_data_season


@dataclass(frozen=True, slots=True)
class HistoricalCatalog:
    sources: tuple[SeasonSource, ...]


def build_catalog(competitions: list[str], seasons: list[str]) -> HistoricalCatalog:
    if not competitions or not seasons:
        raise ValueError("at least one competition and season are required")
    sources = tuple(
        football_data_season(competition, season)
        for competition in competitions
        for season in seasons
    )
    return HistoricalCatalog(sources)
