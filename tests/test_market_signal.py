import pytest

from spm.model.market_signal import build_market_signal


def test_market_signal_requires_streak_and_edge():
    signal = build_market_signal("inter", 5, .40, 3.0, min_streak=4, min_edge=.05)
    assert signal.selected is True


def test_market_signal_rejects_missing_odds():
    with pytest.raises(ValueError, match="odds"):
        build_market_signal("inter", 5, .40, None)
