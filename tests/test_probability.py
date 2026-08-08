import pytest

from spm.statistics.probability import draw_rate, poisson_pmf


def test_draw_rate() -> None:
    assert draw_rate(3, 10) == 0.3


def test_draw_rate_rejects_invalid_counts() -> None:
    with pytest.raises(ValueError):
        draw_rate(1, 0)
    with pytest.raises(ValueError):
        draw_rate(11, 10)


def test_poisson_pmf() -> None:
    assert poisson_pmf(0, 0) == 1.0
    assert poisson_pmf(1, 0) == 0.0
    assert poisson_pmf(0, 1) == pytest.approx(0.36787944117)
