"""Small scheduler adapter for periodic Live refreshes."""
from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Callable

from spm.backtest.oos_ranking import OOSRankingEntry
from spm.live.refresh import refresh_live_report


def run_scheduled_refresh(
    db_path: str | Path,
    oos_entries: list[OOSRankingEntry],
    *,
    output: str | Path,
    analysis_date: date | None = None,
    on_success: Callable[[tuple], None] | None = None,
) -> tuple:
    """Run one refresh cycle; external cron/GitHub Actions can invoke this function."""
    result = refresh_live_report(
        db_path,
        oos_entries,
        output=output,
        as_of=analysis_date,
    )
    if on_success:
        on_success(result)
    return result
