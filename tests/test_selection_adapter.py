from datetime import date

from spm.data.fixtures import Fixture
from spm.live.selection_adapter import to_live_selections
from spm.statistics.engine import SPMScore


def test_adapter_preserves_fixture_date_and_does_not_invent_odds():
    day = date(2026, 8, 25)
    score = SPMScore(" A ", "B", .42, 42.0, .8, .7, .9, (0.6, .15, .15, .1))
    fixture = Fixture("A", "B", day)
    result = to_live_selections([score], [fixture], as_of=date(2026, 8, 24))
    assert len(result) == 1
    assert result[0].fixture_date == day
    assert result[0].draw_odds is None
    assert result[0].probability == .42


def test_adapter_attaches_external_odds_and_oos_score():
    day = date(2026, 8, 25)
    score = SPMScore("A", "B", .42, 42.0, .8, .7, .9, (0.6, .15, .15, .1))
    fixture = Fixture("A", "B", day)
    result = to_live_selections(
        [score], [fixture], as_of=date(2026, 8, 24),
        oos_scores={"A|B": 60.0}, draw_odds={(day, "A", "B"): 3.2},
    )
    assert result[0].draw_odds == 3.2
    assert result[0].oos_score == 60.0
    assert result[0].combined_score == 51.0
