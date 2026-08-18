from datetime import date

from spm.backtest.dataset import group_by_competition_season
from spm.data.normalized import MatchRecord


def test_group_by_competition_season_sorts_each_group():
    records = [
        MatchRecord(date(2025, 8, 3), "C", "D", 1, 0, "I1", "2526"),
        MatchRecord(date(2025, 8, 1), "A", "B", 0, 0, "I1", "2526"),
        MatchRecord(date(2025, 8, 2), "E", "F", 2, 1, "E0", "2526"),
    ]
    groups = group_by_competition_season(records)
    assert set(groups) == {("I1", "2526"), ("E0", "2526")}
    assert groups[("I1", "2526")][0].date == date(2025, 8, 1)
