from datetime import date

import pytest

from spm.backtest.market_runner import MarketBacktestObservation
from spm.backtest.oos_evaluation import evaluate_oos


def test_oos_metrics_use_market_prices_without_future_results():
    rows = (
        MarketBacktestObservation(date(2026, 1, 1), "A", "B", .40, True, True, 3.0),
        MarketBacktestObservation(date(2026, 1, 2), "A", "C", .20, False, False, 3.0),
        MarketBacktestObservation(date(2026, 1, 3), "D", "E", .50, False, False, None),
    )
    metrics = evaluate_oos(rows, min_edge=.05)
    assert metrics.observations == 3
    assert metrics.priced == 2
    assert metrics.selected == 1
    assert metrics.selected_draw_rate == 1.0
    assert metrics.mean_edge == pytest.approx((.40 - 1/3 + .20 - 1/3) / 2)


def test_negative_edge_threshold_rejected():
    with pytest.raises(ValueError):
        evaluate_oos([], min_edge=-.01)
