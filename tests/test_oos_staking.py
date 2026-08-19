from datetime import date, timedelta

from spm.backtest.market_runner import MarketBacktestObservation
from spm.backtest.oos_staking import evaluate_oos_staking_windows


def test_staking_is_applied_only_to_test_window():
    rows = tuple(
        MarketBacktestObservation(
            date(2026, 1, 1) + timedelta(days=i),
            "A", "B", .50 if i < 4 else .20,
            i in (0, 1, 4), True, 3.0
        )
        for i in range(6)
    )
    results = evaluate_oos_staking_windows(
        rows, [0.0, .1], train_size=4, test_size=2,
        initial_bankroll=100.0, base_stake=10.0,
    )
    assert len(results) == 1
    assert results[0].window.test_start == 4
    assert results[0].bets <= 2
