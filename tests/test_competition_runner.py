from datetime import date

from spm.backtest.competition_runner import run_by_competition
from spm.data.normalized import MatchRecord


def test_backtest_isolated_by_competition():
    records = [
        MatchRecord(date(2025, 1, 1), "A", "B", 1, 0, "I1", "2526"),
        MatchRecord(date(2025, 1, 2), "A", "B", 0, 0, "E0", "2526"),
        MatchRecord(date(2025, 1, 3), "B", "A", 0, 0, "I1", "2526"),
        MatchRecord(date(2025, 1, 4), "B", "A", 1, 1, "I1", "2526"),
    ]
    result = run_by_competition(records, min_history=1)
    assert set(result) == {"E0", "I1"}
    assert len(result["E0"]) == 0
    assert len(result["I1"]) == 2
