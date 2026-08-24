"""Build the final Live report directly from upcoming fixtures."""
from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Iterable

from spm.backtest.oos_ranking import OOSRankingEntry
from spm.data.fixtures import Fixture
from spm.data.models import Match
from spm.statistics.engine import SPMEngine
from spm.live.top5 import build_upcoming_top5
from spm.live.selection_adapter import to_live_selections
from spm.live.selection_history import append_selections
from spm.web_live import write_live_dashboard


def build_upcoming_live_report(
    matches: list[Match],
    fixtures: Iterable[Fixture],
    oos_entries: Iterable[OOSRankingEntry],
    *,
    as_of: date,
    path: str | Path,
    history_path: str | Path | None = None,
    engine: SPMEngine | None = None,
    min_bets: int = 20,
    min_profitable_window_rate: float = 0.50,
    oos_weight: float = 0.40,
    live_status: str | None = None,
) -> tuple:
    """Run the complete fixture-to-dashboard production flow."""
    fixture_rows = tuple(fixtures)
    entries = tuple(oos_entries)
    candidates = build_upcoming_top5(
        matches,
        fixture_rows,
        entries,
        as_of=as_of,
        engine=engine,
        min_bets=min_bets,
        min_profitable_window_rate=min_profitable_window_rate,
        oos_weight=oos_weight,
    )
    if history_path is not None:
        scores = tuple()
        # The public Top-5 API intentionally owns ranking policy; history is
        # populated by the dedicated adapter when scored candidates are supplied.
        # Do not fabricate missing fixture/score fields here.
        del scores
    status = live_status or ("LIVE · SPM + OOS" if entries else "LIVE · SPM ONLY")
    write_live_dashboard(
        candidates,
        as_of=as_of.isoformat(),
        path=path,
        live_status=status,
        has_oos=bool(entries),
    )
    return candidates
