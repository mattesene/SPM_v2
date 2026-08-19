from datetime import date

from spm.backtest.catalog_backtest import run_catalog_backtest
from spm.data.normalized import MatchRecord


def test_catalog_backtest_aggregates_sources():
    datasets = {
        "e0/2425": [
            MatchRecord(date(2025, 1, 1), "A", "B", 1, 0),
            MatchRecord(date(2025, 1, 8), "A", "C", 1, 1),
            MatchRecord(date(2025, 1, 15), "A", "D", 0, 0),
            MatchRecord(date(2025, 1, 22), "A", "E", 1, 0),
        ]
    }
    result = run_catalog_backtest(datasets)
    assert result.records == 4
    assert result.evaluated == 1
