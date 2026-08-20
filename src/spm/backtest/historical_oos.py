"""Bridge the historical catalog into the rolling OOS backtest."""
from __future__ import annotations

from pathlib import Path

from spm.backtest.pipeline import OOSPipelineResult, evaluate_rolling_oos
from spm.backtest.windows import OOSWindow
from spm.data.historical_catalog import HistoricalCatalog
from spm.data.historical_records import load_historical_records
from spm.data.match_conversion import to_completed_matches


def evaluate_historical_oos(
    catalog: HistoricalCatalog,
    root: str | Path,
    windows: tuple[OOSWindow, ...],
    *,
    odds=(),
    min_history: int = 3,
    threshold: float = 0.0,
    min_streak: int = 3,
    min_edge: float = 0.0,
    min_selections: int = 20,
    top_n: int = 5,
) -> OOSPipelineResult:
    records = load_historical_records(catalog, root)
    matches = to_completed_matches(records)
    if not matches:
        raise ValueError("historical catalog contains no completed matches")
    return evaluate_rolling_oos(
        matches, tuple(odds), windows,
        min_history=min_history,
        threshold=threshold,
        min_streak=min_streak,
        min_edge=min_edge,
        min_selections=min_selections,
        top_n=top_n,
    )
