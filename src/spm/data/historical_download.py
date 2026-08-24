"""Download all sources in a historical catalog into a local cache."""
from __future__ import annotations

from pathlib import Path

from .download import DownloadResult, download_cached
from .historical_catalog import HistoricalCatalog


def download_catalog(catalog: HistoricalCatalog, root: str | Path) -> list[DownloadResult]:
    """Attempt every source and let the caller report unavailable datasets.

    A single stale/removed upstream URL must not abort the whole catalog scan:
    the final completeness check is responsible for identifying missing files.
    """
    root = Path(root)
    results: list[DownloadResult] = []
    for source in catalog.sources:
        destination = root / source.competition / source.season / source.filename
        try:
            results.append(download_cached(source.url, destination))
        except Exception:
            # Keep scanning the catalog. The destination remains absent and is
            # reported by HistoricalPrepareResult.missing.
            continue
    return results
