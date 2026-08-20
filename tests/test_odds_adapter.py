from datetime import date

from spm.data.odds import DrawOdds
from spm.backtest.odds_adapter import attach_odds_to_oos


def test_selected_oos_match_receives_odds():
    class M:
        date = date(2025, 1, 1)
        home_team = "Milan"
        away_team = "Roma"

    class O:
        match = M()
        actual_draw = True
        selected = True

    result = attach_odds_to_oos([O()], [DrawOdds(date(2025, 1, 1), "Milan", "Roma", 3.2, "test")])
    assert result[0].draw_odds == 3.2


def test_unselected_oos_match_does_not_require_odds():
    class M:
        date = date(2025, 1, 1)
        home_team = "Milan"
        away_team = "Roma"

    class O:
        match = M()
        actual_draw = False
        selected = False

    result = attach_odds_to_oos([O()], [])
    assert result[0].draw_odds is None
