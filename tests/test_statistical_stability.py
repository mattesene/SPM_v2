import pytest

from spm.backtest.statistical_stability import binomial_stability


def test_binomial_stability_returns_bounded_interval():
    result = binomial_stability(60, 100)
    assert result.success_rate == .6
    assert result.lower_95 < .6 < result.upper_95
    assert 0 <= result.lower_95 <= result.upper_95 <= 1


def test_invalid_binomial_inputs():
    with pytest.raises(ValueError):
        binomial_stability(1, 0)
    with pytest.raises(ValueError):
        binomial_stability(11, 10)
