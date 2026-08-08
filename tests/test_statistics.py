from datetime import date

import pytest

from spm.data.models import Match
from spm.statistics.probability import draw_rate, poisson_pmf


def test_match_result_and_draw() -> None:
    match = Match(date(2026, 8, 8), "Team A", "Team B", 1, 1)
    assert match.is_draw
    assert match.result == "D"


def test_match_result_home_win() -> None:
    match = Match(date(2026, 8, 8), "Team A", "Team B", 2, 1)
    assert not match.is_draw
    assert match.result == "H"


def test_draw_rate() -> None:
    assert draw_rate(25, 100) == pytest.approx(0.25)


def test_poisson_pmf() -> None:
    assert poisson_pmf(0, 1) == pytest.approx(0.36787944117)
    assert poisson_pmf(1, 1) == pytest.approx(0.36787944117)


def test_invalid_probability_inputs() -> None:
    with pytest.raises(ValueError):
        draw_rate(1, 0)
    with pytest.raises(ValueError):
        poisson_pmf(-1, 1)
