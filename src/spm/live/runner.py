"""Production runner for the persisted-fixture Live report."""
from __future__ import annotations

from datetime import date
from pathlib import Path

from spm.backtest.oos_ranking import OOSRankingEntry
from spm.data.repository import MatchRepository
from spm.live.data_manifest import validate_live_inputs
from spm.live.data_quality import assess_live_data
from spm.live.report import build_upcoming_live_report


def run_live_from_database(
    db_path: str | Path,
    oos_entries: list[OOSRankingEntry],
    *,
    as_of: date,
    output: str | Path,
    oos_path: str | Path | None = None,
    max_match_age_days: int | None = None,
) -> tuple:
    """Load Live inputs, enforce quality gates, and build the report.

    Live fixtures are current, while the model's completed matches are the
    historical training corpus.  Recency of completed matches is therefore
    opt-in rather than a production requirement.
    """
    if oos_path is not None:
        validate_live_inputs(db_path, oos_path)
    else:
        db = Path(db_path)
        if not db.is_file() or db.stat().st_size == 0:
            raise FileNotFoundError(f"Live database not found or empty: {db}")

    repository = MatchRepository(db_path)
    matches = repository.load_matches(completed_only=True)
    fixtures = repository.load_fixtures(from_date=as_of)
    print(
        "live_inputs,"
        f"as_of={as_of.isoformat()},matches={len(matches)},fixtures={len(fixtures)},"
        f"fixture_dates={[fixture.date.isoformat() for fixture in fixtures]}"
    )
    print(
        "live_fixture_rows="
        + repr([(fixture.home_team, fixture.away_team, fixture.date.isoformat()) for fixture in fixtures])
    )
    quality = assess_live_data(
        matches,
        fixtures,
        as_of=as_of,
        max_match_age_days=max_match_age_days,
    )
    if not quality.ok:
        details = "; ".join(quality.warnings) or "unknown data-quality failure"
        raise RuntimeError(f"Live data quality gate failed: {details}")

    candidates = build_upcoming_live_report(
        matches,
        fixtures,
        oos_entries,
        as_of=as_of,
        path=output,
    )
    print(f"live_output,candidates={len(candidates)},output={output}")
    return candidates
