from spm.backtest.market_selection import select_market_signal


def test_market_selection_requires_odds():
    assert select_market_signal("inter", 5, .40, None) is None


def test_market_selection_applies_streak_and_edge():
    signal = select_market_signal("inter", 5, .40, 3.0, min_streak=4, min_edge=.05)
    assert signal is not None
    assert signal.selected is True
