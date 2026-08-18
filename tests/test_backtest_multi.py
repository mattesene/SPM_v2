from datetime import date

from spm.backtest.multi import run_multi
from spm.data.normalized import MatchRecord


class DummyEngine:
    def predict(self, home_team, away_team):
        return None

    def update(self, home_team, away_team, home_goals, away_goals):
        pass


def test_run_multi_isolates_each_slice():
    records = [
        MatchRecord(date(2025, 8, 2), "C", "D", 1, 0, "E0", "2526"),
        MatchRecord(date(2025, 8, 1), "A", "B", 0, 0, "I1", "2526"),
    ]
    report = run_multi(records, DummyEngine)
    assert [(x.competition, x.season) for x in report.slices] == [("E0", "2526"), ("I1", "2526")]
    assert report.total_samples == 0
    assert report.accuracy == 0.0
