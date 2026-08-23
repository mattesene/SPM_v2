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
from spm.web_live import write_live_dashboard


def build_upcoming_live_report(
    matches: list[Match],
    fixtures: Iterable[Fixture],
    oos_entries: Iterable[OOSRankingEntry],
    *,
    as_of: date,
    path: str | Path,
    engine: SPMEngine | None = None,
    min_bets: int = 20,
    min_profitable_window_rate: float = 0.50,
    oos_weight: float = 0.40,
) -> tuple:
    """Run the complete fixture-to-dashboard production flow."""
    candidates = build_upcoming_top5(
        matches,
        fixtures,
        oos_entries,
        as_of=as_of,
        engine=engine,
        min_bets=min_bets,
        min_profitable_window_rate=min_profitable_window_rate,
        oos_weight=oos_weight,
    )
    write_live_dashboard(candidates, as_of=as_of.isoformat(), path=path)
    return candidates
