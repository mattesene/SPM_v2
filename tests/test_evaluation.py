import pytest

from spm.statistics.evaluation import probability_metrics


def test_probability_metrics() -> None:
    metrics = probability_metrics([0.8, 0.2], [True, False])
    assert metrics.brier_score == pytest.approx(0.04)
    assert metrics.log_loss > 0
