from datetime import date

from spm.backtest.oos_ranking import OOSRankingEntry
from spm.data.fixtures import Fixture
from spm.data.models import Match
from spm.live.top5 import build_upcoming_top5


def test_build_upcoming_top5_ignores_past_fixtures() -> None:
    matches = [
        Match(date(2026, 8, 1), "H0", "A0", 1, 1),
        Match(date(2026, 8, 2), "H1", "A1", 0, 0),
    ]
    fixtures = [
        Fixture(date(2026, 8, 24), "H0", "A0"),
        Fixture(date(2026, 8, 25), "H1", "A1"),
        Fixture(date(2026, 8, 20), "OLD", "TEAM"),
    ]
    evidence = [
        OOSRankingEntry("H0 vs A0", 20, 100.0, .10, .80, 0, 0, 0),
        OOSRankingEntry("H1 vs A1", 20, 90.0, .10, .80, 0, 0, 0),
    ]
    result = build_upcoming_top5(matches, fixtures, evidence, as_of=date(2026, 8, 23))
    assert len(result) <= 5
    assert all(item.bets >= 20 for item in result)
