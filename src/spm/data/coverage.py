"""Coverage validation for historical competition/season catalogs."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .historical_catalog import HistoricalCatalog


@dataclass(frozen=True, slots=True)
class CoverageReport:
    expected: int
    present: int
    missing: tuple[tuple[str, str], ...]

    @property
    def complete(self) -> bool:
        return not self.missing


def validate_catalog_coverage(catalog: HistoricalCatalog, root: str | Path) -> CoverageReport:
    root = Path(root)
    missing: list[tuple[str, str]] = []
    for source in catalog.sources:
        path = root / source.competition / source.season / source.filename
        if not path.exists():
            missing.append((source.competition, source.season))
    return CoverageReport(len(catalog.sources), len(catalog.sources) - len(missing), tuple(missing))
