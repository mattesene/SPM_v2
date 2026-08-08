import pytest

from spm.statistics.calibration import calibrate_weights


def test_calibration_weights_sum_to_one_and_reduce_error() -> None:
    features = [
        (0.9, 0.2, 0.1),
        (0.8, 0.3, 0.2),
        (0.1, 0.8, 0.7),
        (0.2, 0.7, 0.8),
    ]
    outcomes = [True, True, False, False]
    result = calibrate_weights(features, outcomes, step=0.1)
    assert sum(result.weights) == pytest.approx(1.0)
    assert result.brier_score < 0.25


def test_calibration_rejects_bad_input() -> None:
    with pytest.raises(ValueError):
        calibrate_weights([], [])
    with pytest.raises(ValueError):
        calibrate_weights([(0.1, 0.2)], [])
