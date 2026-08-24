from datetime import date

from spm.backtest.time_split import split_train_oos
from spm.data.models import Match
from spm.data.odds import DrawOdds


def test_split_matches_and_odds_with_same_cutoff():
    matches = [
        Match(date(2026, 8, 3), "C", "D", 1, 0),
        Match(date(2026, 8, 1), "A", "B", 1, 1),
        Match(date(2026, 8, 2), "A", "C", 0, 1),
    ]
    odds = [
        DrawOdds(date(2026, 8, 1), "A", "B", 3.0),
        DrawOdds(date(2026, 8, 3), "C", "D", 2.5),
    ]
    split = split_train_oos(matches, odds, date(2026, 8, 3))
    assert [m.date for m in split.train] == [date(2026, 8, 1), date(2026, 8, 2)]
    assert [m.date for m in split.oos] == [date(2026, 8, 3)]
    assert [o.date for o in split.train_odds] == [date(2026, 8, 1)]
    assert [o.date for o in split.oos_odds] == [date(2026, 8, 3)]
