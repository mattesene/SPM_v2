from datetime import date

import pytest

from spm.backtest.edge_staking import run_edge_staking
from spm.backtest.market_runner import MarketBacktestObservation


def test_edge_is_applied_before_staking():
    rows = (
        MarketBacktestObservation(date(2026, 1, 1), "A", "B", .40, True, True, 3.0),
        MarketBacktestObservation(date(2026, 1, 2), "A", "C", .20, True, True, 3.0),
        MarketBacktestObservation(date(2026, 1, 3), "D", "E", .50, False, True, None),
    )
    result = run_edge_staking(rows, min_edge=.05, initial_bankroll=100, base_stake=10)
    assert result.priced == 2
    assert result.selected == 1
    assert result.positive_edge == 1
    assert result.staking.bets == 1


def test_negative_edge_threshold_rejected():
    with pytest.raises(ValueError):
        run_edge_staking([], min_edge=-.01)
