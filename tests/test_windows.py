from datetime import date

from spm.backtest.windows import build_rolling_windows


def test_build_rolling_windows():
    windows = build_rolling_windows([date(2019,1,1), date(2025,12,31)], train_years=3, validation_years=1, oos_years=1)
    assert windows[0].train_start == date(2019,1,1)
    assert windows[0].oos_start == date(2023,1,1)
    assert windows[-1].oos_end <= date(2026,1,1)
