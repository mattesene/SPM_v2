"""Validated default historical scope for the SPM backtest."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .default_historical_catalog import default_catalog
from .historical_catalog import HistoricalCatalog


@dataclass(frozen=True, slots=True)
class HistoricalScope:
    catalog: HistoricalCatalog
    root: Path

    @property
    def expected_files(self) -> tuple[Path, ...]:
        return tuple(
            self.root / source.competition / source.season / source.filename
            for source in self.catalog.sources
        )

    @property
    def missing_files(self) -> tuple[Path, ...]:
        return tuple(path for path in self.expected_files if not path.is_file())

    @property
    def complete(self) -> bool:
        return not self.missing_files


def default_historical_scope(root: str | Path, *, start_season: int = 2019, end_season: int = 2025) -> HistoricalScope:
    if start_season >= end_season:
        raise ValueError("start_season must be before end_season")
    return HistoricalScope(default_catalog(start_season, end_season), Path(root))
