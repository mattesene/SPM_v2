import pytest

from spm.backtest.odds_staking import simulate_draw_progression_with_odds


def test_missing_odds_are_skipped_without_advancing_progression():
    result = simulate_draw_progression_with_odds(
        [("Team A", False, 2.0), ("Team A", False, None), ("Team A", True, 3.0)],
        initial_bankroll=100.0,
        base_stake=10.0,
    )
    assert result.bets == 2
    assert result.skipped == 1
    assert result.wins == 1
    assert result.final_bankroll == pytest.approx(110.0)


def test_progressions_are_independent_by_team():
    result = simulate_draw_progression_with_odds(
        [("A", False, 2.0), ("B", False, 2.0), ("A", True, 3.0)],
        initial_bankroll=100.0,
        base_stake=10.0,
    )
    assert result.bets == 3
    assert result.wins == 1
    assert result.final_bankroll == pytest.approx(110.0)


def test_invalid_odds_are_rejected():
    with pytest.raises(ValueError):
        simulate_draw_progression_with_odds(
            [("A", True, 1.0)], initial_bankroll=100.0, base_stake=10.0
        )
