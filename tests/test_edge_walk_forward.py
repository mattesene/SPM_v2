from datetime import date, timedelta

from spm.backtest.edge_walk_forward import run_edge_walk_forward
from spm.backtest.market_runner import MarketBacktestObservation


def test_walk_forward_selects_threshold_only_from_train_window():
    rows = tuple(
        MarketBacktestObservation(
            date(2026, 1, 1) + timedelta(days=i),
            "A", "B", .50 if i < 4 else .20,
            i in (0, 1, 4), True, 3.0
        )
        for i in range(6)
    )
    windows = run_edge_walk_forward(rows, [0.0, 0.1, 0.2], train_size=4, test_size=2)
    assert len(windows) == 1
    assert windows[0].train_end == windows[0].test_start
    assert windows[0].test_end == 6
    assert windows[0].threshold in {0.0, 0.1, 0.2}
