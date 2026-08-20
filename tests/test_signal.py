import pytest

from spm.model.signal import build_signal


def test_signal_requires_streak_and_positive_edge():
    selected = build_signal("inter", 5, .40, 3.0, min_streak=4, min_edge=.05)
    assert selected.selected is True


def test_signal_rejects_insufficient_streak():
    signal = build_signal("inter", 2, .40, 3.0, min_streak=4, min_edge=.05)
    assert signal.selected is False


def test_signal_rejects_negative_streak():
    with pytest.raises(ValueError):
        build_signal("inter", -1, .4, 3.0)
