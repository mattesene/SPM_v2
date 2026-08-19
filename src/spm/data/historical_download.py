"""Download all sources in a historical catalog into a local cache."""
from __future__ import annotations

from pathlib import Path

from .download import DownloadResult, download_cached
from .historical_catalog import HistoricalCatalog


def download_catalog(catalog: HistoricalCatalog, root: str | Path) -> list[DownloadResult]:
    root = Path(root)
    results: list[DownloadResult] = []
    for source in catalog.sources:
        destination = root / source.competition / source.season / source.filename
        results.append(download_cached(source.url, destination))
    return results
