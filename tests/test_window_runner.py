from datetime import date

from spm.backtest.market_runner import MarketBacktestObservation
from spm.backtest.window_runner import run_oos_windows
from spm.backtest.windows import OOSWindow


def test_empty_oos_window_is_skipped():
    window = OOSWindow(date(2020,1,1), date(2022,1,1), date(2023,1,1), date(2023,1,1), date(2024,1,1))
    assert run_oos_windows([], [], [window]) == ()
