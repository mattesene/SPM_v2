"""Safe periodic refresh helpers for the Live dashboard."""
from __future__ import annotations

from datetime import date
from pathlib import Path

from spm.backtest.oos_ranking import OOSRankingEntry
from spm.live.runner import run_live_from_database


def refresh_live_report(
    db_path: str | Path,
    oos_entries: list[OOSRankingEntry],
    *,
    output: str | Path,
    as_of: date | None = None,
) -> tuple:
    """Regenerate the Live dashboard using today's analysis date by default."""
    analysis_date = as_of or date.today()
    return run_live_from_database(db_path, oos_entries, as_of=analysis_date, output=output)
