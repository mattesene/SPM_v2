import pytest

from spm.backtest.odds_staking import simulate_draw_progression_with_odds


def test_drawdown_is_measured_from_previous_peak():
    result = simulate_draw_progression_with_odds(
        [("A", False, 2.0), ("A", False, 2.0), ("A", True, 4.0)],
        initial_bankroll=100.0,
        base_stake=10.0,
    )
    # 100 -> 90 -> 70 -> 150; largest peak-to-trough decline is 30.
    assert result.max_drawdown == pytest.approx(30.0)


def test_profit_matches_final_bankroll_minus_initial_bankroll():
    result = simulate_draw_progression_with_odds(
        [("A", True, 3.0)],
        initial_bankroll=100.0,
        base_stake=10.0,
    )
    assert result.profit == pytest.approx(result.final_bankroll - 100.0)
