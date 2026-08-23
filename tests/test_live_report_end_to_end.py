from datetime import date

from spm.backtest.oos_ranking import OOSRankingEntry
from spm.data.fixtures import Fixture
from spm.data.models import Match
from spm.live.report import build_upcoming_live_report


def test_build_upcoming_live_report_creates_dashboard(tmp_path) -> None:
    matches = [
        Match("H0", "A0", date(2026, 8, 1), 1, 1),
        Match("H1", "A1", date(2026, 8, 2), 0, 0),
    ]
    fixtures = [
        Fixture("H0", "A0", date(2026, 8, 24)),
        Fixture("H1", "A1", date(2026, 8, 25)),
    ]
    evidence = [
        OOSRankingEntry("H0 vs A0", 20, 100.0, .10, .80, 0, 0, 0),
        OOSRankingEntry("H1 vs A1", 20, 90.0, .10, .80, 0, 0, 0),
    ]
    output = tmp_path / "live.html"
    result = build_upcoming_live_report(
        matches, fixtures, evidence, as_of=date(2026, 8, 23), path=output
    )
    assert output.exists()
    assert len(result) <= 5
    html = output.read_text(encoding="utf-8")
    assert "SPM_v2 · Live" in html
