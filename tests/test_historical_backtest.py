from datetime import date, timedelta

from spm.backtest.historical import run_historical_backtest
from spm.data.models import Match


def test_historical_backtest_uses_only_prior_matches():
    start = date(2025, 1, 1)
    matches = [
        Match(start + timedelta(days=i), "A", "B", 1, 0) for i in range(3)
    ]
    report = run_historical_backtest(matches, min_history=1, threshold=0.0)
    assert report.samples == 2
    assert report.brier is not None


def test_historical_backtest_is_order_independent():
    start = date(2025, 1, 1)
    matches = [
        Match(start, "A", "B", 1, 1),
        Match(start + timedelta(days=1), "B", "A", 0, 1),
        Match(start + timedelta(days=2), "A", "B", 0, 0),
    ]
    ordered = run_historical_backtest(matches, min_history=1)
    reversed_report = run_historical_backtest(list(reversed(matches)), min_history=1)
    assert ordered == reversed_report
