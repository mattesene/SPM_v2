from datetime import date

from spm.backtest.oos_ranking import OOSRankingEntry
from spm.data.fixtures import Fixture
from spm.live.report import build_upcoming_live_report
from spm.statistics.engine import SPMEngine, SPMScore


class FakeEngine(SPMEngine):
    def score(self, matches, home_team, away_team, as_of):
        return SPMScore(home_team, away_team, .30, 80.0, .75, .70, .65, (.55, .25, .20, .10))


def test_live_report_writes_html(tmp_path):
    output = tmp_path / "live.html"
    fixtures = [Fixture(date(2026, 8, 24), "Team A", "Team B")]
    oos = [OOSRankingEntry("Team A vs Team B", 30, 20, 80.0, .10, 0.0, .75, 1.0)]
    result = build_upcoming_live_report([], fixtures, oos, as_of=date(2026, 8, 23), path=output, engine=FakeEngine())
    assert len(result) == 1
    html = output.read_text(encoding="utf-8")
    assert "Team A" in html
    assert "Team B" in html
    assert "LIVE AGGIORNATO" in html
