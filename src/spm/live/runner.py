"""Production runner for the persisted-fixture Live report."""
from __future__ import annotations

from datetime import date
from pathlib import Path

from spm.backtest.oos_ranking import OOSRankingEntry
from spm.data.repository import MatchRepository
from spm.live.data_manifest import validate_live_inputs
from spm.live.report import build_upcoming_live_report


def run_live_from_database(
    db_path: str | Path,
    oos_entries: list[OOSRankingEntry],
    *,
    as_of: date,
    output: str | Path,
    oos_path: str | Path | None = None,
) -> tuple:
    """Load completed matches and future fixtures and build the report safely."""
    if oos_path is not None:
        validate_live_inputs(db_path, oos_path)
    else:
        db = Path(db_path)
        if not db.is_file() or db.stat().st_size == 0:
            raise FileNotFoundError(f"Live database not found or empty: {db}")

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
