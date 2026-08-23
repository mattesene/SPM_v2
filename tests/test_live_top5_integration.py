from datetime import date

from spm.backtest.live_selection import LiveCandidate
from spm.backtest.oos_ranking import OOSRankingEntry
from spm.data.fixtures import Fixture
from spm.data.models import Match
from spm.live.top5 import build_upcoming_top5
from spm.statistics.engine import SPMEngine, SPMScore


class FakeEngine(SPMEngine):
    def score(self, matches, home_team, away_team, as_of):
        return SPMScore(home_team, away_team, .30, 80.0, .75, .70, .65, (.55, .25, .20, .10))


def test_upcoming_top5_runs_fixture_scoring_and_oos_selection():
    fixtures = [
        Fixture(date(2026, 8, 24), "Team A", "Team B"),
        Fixture(date(2026, 8, 25), "Team C", "Team D"),
    ]
    oos = [
        OOSRankingEntry("Team A vs Team B", 2, 30, 100.0, .10, .0, .75, 1.0),
        OOSRankingEntry("Team C vs Team D", 2, 30, 100.0, .20, .0, .70, 1.0),
    ]
    result = build_upcoming_top5([], fixtures, oos, as_of=date(2026, 8, 23), engine=FakeEngine())
    assert len(result) == 2
    assert all(isinstance(item, LiveCandidate) for item in result)
    assert result[0].fixture == ("Team A", "Team B")
