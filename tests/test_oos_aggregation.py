from datetime import date

from spm.backtest.oos_aggregation import aggregate_oos_results
from spm.backtest.window_runner import WindowResult
from spm.backtest.windows import OOSWindow
from spm.backtest.market_runner import MarketBacktestObservation


def test_aggregate_oos_results_counts_only_real_selections():
    window = OOSWindow(date(2020,1,1), date(2020,2,1), date(2020,2,1), date(2020,3,1), date(2020,3,1))
    observations = (
        MarketBacktestObservation(date(2020,2,2), "A", "B", 3, True, True, 3.2),
        MarketBacktestObservation(date(2020,2,3), "C", "D", 2, True, False, 3.1),
        MarketBacktestObservation(date(2020,2,4), "E", "F", 4, False, False, None),
    )
    result = aggregate_oos_results((WindowResult(window, observations, ()),))
    assert result.windows == 1
    assert result.observations == 3
    assert result.selected == 1
    assert result.draws == 1
    assert result.hit_rate == 1.0
