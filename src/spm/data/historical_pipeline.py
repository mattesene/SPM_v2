"""Reproducible download, validation and loading of the historical scope."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .historical_download import DownloadResult, download_catalog
from .historical_scope import HistoricalScope


@dataclass(frozen=True, slots=True)
class HistoricalPrepareResult:
    downloads: tuple[DownloadResult, ...]
    missing: tuple[Path, ...]

    @property
    def complete(self) -> bool:
        return not self.missing


def prepare_historical_scope(scope: HistoricalScope) -> HistoricalPrepareResult:
    """Download/cache the complete catalog and fail only after checking every source."""
    downloads = tuple(download_catalog(scope.catalog, scope.root))
    missing = tuple(path for path in scope.expected_files if not path.is_file())
    return HistoricalPrepareResult(downloads, missing)
