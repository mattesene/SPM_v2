from datetime import date

from spm.data.normalized import MatchRecord
from spm.backtest.historical_runner import run_historical_backtest


def test_historical_runner_preserves_chronological_backtest_rules():
    records = [
        MatchRecord(date(2025, 1, 1), "A", "B", 1, 0, "I1", "2526"),
        MatchRecord(date(2025, 1, 2), "B", "C", 1, 1, "I1", "2526"),
        MatchRecord(date(2025, 1, 3), "C", "A", 0, 0, "I1", "2526"),
        MatchRecord(date(2025, 1, 4), "A", "B", 2, 1, "I1", "2526"),
    ]
    result = run_historical_backtest(records, min_history=3)
    assert len(result) == 1
    assert result[0].home_team == "A"
    assert result[0].away_team == "B"
