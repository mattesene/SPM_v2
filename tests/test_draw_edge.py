import pytest

from spm.model.draw_edge import calculate_draw_edge


def test_draw_edge_uses_market_implied_probability():
    result = calculate_draw_edge(.40, 3.0)
    assert result.implied_probability == pytest.approx(1 / 3)
    assert result.edge == pytest.approx(.40 - 1 / 3)


def test_draw_edge_rejects_invalid_values():
    with pytest.raises(ValueError):
        calculate_draw_edge(1.1, 3.0)
    with pytest.raises(ValueError):
        calculate_draw_edge(.4, 1.0)
