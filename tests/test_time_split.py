from datetime import date

from spm.backtest.time_split import split_train_oos
from spm.data.models import Match


def test_split_is_strictly_chronological():
    matches = [
        Match(date(2026, 8, 3), "C", "D", 1, 0),
        Match(date(2026, 8, 1), "A", "B", 1, 1),
        Match(date(2026, 8, 2), "A", "C", 0, 1),
    ]
    split = split_train_oos(matches, date(2026, 8, 3))
    assert [m.date for m in split.train] == [date(2026, 8, 1), date(2026, 8, 2)]
    assert [m.date for m in split.oos] == [date(2026, 8, 3)]


def test_cutoff_match_belongs_to_oos_not_train():
    match = Match(date(2026, 8, 3), "A", "B", 1, 1)
    split = split_train_oos([match], date(2026, 8, 3))
    assert not split.train
    assert split.oos == (match,)
