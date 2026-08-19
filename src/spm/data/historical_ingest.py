"""End-to-end historical ingestion orchestration."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .historical_catalog import HistoricalCatalog
from .historical_download import download_catalog
from .historical_loader import load_catalog


@dataclass(frozen=True, slots=True)
class IngestionResult:
    downloaded: int
    cached: int
    datasets: dict[tuple[str, str], object]


def ingest_catalog(catalog: HistoricalCatalog, root: str | Path) -> IngestionResult:
    results = download_catalog(catalog, root)
    datasets = load_catalog(catalog, root)
    return IngestionResult(
        downloaded=sum(item.downloaded for item in results),
        cached=sum(not item.downloaded for item in results),
        datasets=datasets,
    )
