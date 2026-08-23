from datetime import date

from spm.backtest.oos_ranking import OOSRankingEntry
from spm.data.fixtures import Fixture
from spm.data.models import Match
from spm.data.repository import MatchRepository
from spm.live.scheduler import run_scheduled_refresh


def test_scheduled_refresh_calls_success_callback(tmp_path) -> None:
    db = tmp_path / "spm.db"
    repo = MatchRepository(db)
    repo.upsert_match(Match("H0", "A0", date(2026, 8, 1), 1, 1))
    repo.upsert_match(Match("H1", "A1", date(2026, 8, 2), 0, 0))
    repo.upsert_fixture(Fixture("H0", "A0", date(2026, 8, 24)))
    repo.upsert_fixture(Fixture("H1", "A1", date(2026, 8, 25)))
    evidence = [
        OOSRankingEntry("H0 vs A0", 20, 100.0, .10, .80, 0, 0, 0),
        OOSRankingEntry("H1 vs A1", 20, 90.0, .10, .80, 0, 0, 0),
    ]
    output = tmp_path / "live.html"
    calls = []
    result = run_scheduled_refresh(
        db, evidence, output=output, analysis_date=date(2026, 8, 23), on_success=calls.append
    )
    assert output.exists()
    assert calls == [result]
