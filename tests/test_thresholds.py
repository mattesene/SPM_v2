from datetime import date

import pytest

from spm.backtest.market_runner import MarketBacktestObservation
from spm.backtest.thresholds import evaluate_thresholds


def test_threshold_sensitivity_does_not_change_source_observations():
    rows = (
        MarketBacktestObservation(date(2026, 1, 1), "A", "B", .30, True, False, 3.0),
        MarketBacktestObservation(date(2026, 1, 2), "A", "C", .70, True, False, 3.1),
        MarketBacktestObservation(date(2026, 1, 3), "D", "E", .90, False, False, None),
    )
    results = evaluate_thresholds(rows, [.5, .8])
    assert [item.selected for item in results] == [2, 1]
    assert [item.priced_selected for item in results] == [2, 0]
    assert rows[0].selected is False


def test_invalid_threshold_is_rejected():
    with pytest.raises(ValueError):
        evaluate_thresholds([], [1.1])
