from datetime import date

from spm.data.fixtures import Fixture
from spm.live.selection_adapter import to_live_selections
from spm.statistics.engine import SPMScore


def test_adapter_preserves_fixture_date_and_odds():
    day = date(2026, 8, 25)
    score = SPMScore(" A ", "B", .42, 42.0, .8, .7, .9, (0.6, .15, .15, .1))
    fixture = Fixture("A", "B", day, draw_odds=3.2)
    result = to_live_selections([score], [fixture], as_of=date(2026, 8, 24))
    assert len(result) == 1
    assert result[0].fixture_date == day
    assert result[0].draw_odds == 3.2
    assert result[0].probability == .42


def test_adapter_can_attach_oos_score():
    day = date(2026, 8, 25)
    score = SPMScore("A", "B", .42, 42.0, .8, .7, .9, (0.6, .15, .15, .1))
    fixture = Fixture("A", "B", day, draw_odds=3.2)
    result = to_live_selections([score], [fixture], as_of=date(2026, 8, 24), oos_scores={"A|B": 60.0})
    assert result[0].oos_score == 60.0
    assert result[0].combined_score == 51.0
