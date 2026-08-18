from datetime import date

from spm.backtest.historical_batch import run_historical_batch
from spm.data.normalized import MatchRecord


def test_historical_batch_runs_independent_sources():
    records = [
        MatchRecord(date(2025, 1, 1), "A", "B", 1, 0),
        MatchRecord(date(2025, 1, 8), "A", "C", 1, 1),
    ]
    result = run_historical_batch({"season-a": records}, min_history=1)
    assert result[0].path == "season-a"
    assert result[0].records == 2
    assert result[0].evaluated == 2
    assert result[0].not_evaluated == 0
