"""Production runner for the persisted-fixture Live report."""
from __future__ import annotations

from datetime import date
from pathlib import Path

from spm.backtest.oos_ranking import OOSRankingEntry
from spm.data.repository import MatchRepository
from spm.live.report import build_upcoming_live_report


def run_live_from_database(
    db_path: str | Path,
    oos_entries: list[OOSRankingEntry],
    *,
    as_of: date,
    output: str | Path,
) -> tuple:
    """Load completed matches and future fixtures from SQLite and build the report."""
    repository = MatchRepository(db_path)
    matches = repository.load_matches(completed_only=True)
    fixtures = repository.load_fixtures(from_date=as_of)
    return build_upcoming_live_report(
        matches,
        fixtures,
        oos_entries,
        as_of=as_of,
        path=output,
    )
