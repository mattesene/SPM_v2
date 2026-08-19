import pytest

from spm.backtest.edge import calculate_edge, evaluate_market_edge
from spm.backtest.market_runner import MarketBacktestObservation
from datetime import date


def test_calculate_edge_against_market_probability():
    assert calculate_edge(0.40, 3.0) == pytest.approx(1 / 15)


def test_edge_selection_uses_only_priced_matches():
    rows = (
        MarketBacktestObservation(date(2026, 1, 1), "A", "B", .40, True, False, 3.0),
        MarketBacktestObservation(date(2026, 1, 2), "A", "C", .25, False, False, None),
    )
    result = evaluate_market_edge(rows, min_edge=.05)
    assert len(result) == 1
    assert result[0].selected is True


def test_negative_edge_threshold_is_rejected():
    with pytest.raises(ValueError):
        evaluate_market_edge([], min_edge=-.01)
