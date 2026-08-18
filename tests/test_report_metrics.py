import pytest

from spm.backtest.report_metrics import brier_score, flat_stake_roi, log_loss


def test_brier_score():
    assert brier_score([0.5, 0.9], [1, 0]) == pytest.approx(0.53)


def test_log_loss_is_finite_at_extremes():
    assert log_loss([1.0, 0.0], [1, 0]) < 1e-10


def test_flat_stake_roi_is_selection_hit_rate_proxy():
    assert flat_stake_roi([1, 1, 0], [1, 0, 1]) == pytest.approx(0.5)


def test_probability_length_mismatch():
    with pytest.raises(ValueError):
        brier_score([0.5], [1, 0])


def test_invalid_probability():
    with pytest.raises(ValueError):
        log_loss([1.1], [1])
