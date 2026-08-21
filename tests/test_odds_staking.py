import pytest

from spm.backtest.odds_staking import simulate_draw_progression_with_odds


def test_odds_staking_uses_match_specific_price_and_resets_on_draw():
    result = simulate_draw_progression_with_odds(
        [("Milan", False, 3.0), ("Milan", True, 3.5)],
        initial_bankroll=100.0,
        base_stake=10.0,
    )
    assert result.bets == 2
    assert result.wins == 1
    assert result.final_bankroll == pytest.approx(160.0)


def test_missing_odds_are_skipped_without_changing_progression():
    result = simulate_draw_progression_with_odds(
        [("Milan", False, 3.0), ("Milan", True, None), ("Milan", True, 3.0)],
        initial_bankroll=100.0,
        base_stake=10.0,
    )
    assert result.skipped == 1
    assert result.bets == 2
    assert result.final_bankroll == pytest.approx(150.0)


def test_progressions_are_independent_per_team():
    result = simulate_draw_progression_with_odds(
        [("Milan", False, 3.0), ("Inter", False, 3.0), ("Milan", True, 3.0)],
        initial_bankroll=100.0,
        base_stake=10.0,
    )
    assert result.bets == 3
    assert result.wins == 1
    assert result.final_bankroll == pytest.approx(140.0)


def test_invalid_odds_are_rejected():
    with pytest.raises(ValueError):
        simulate_draw_progression_with_odds(
            [("Milan", True, 1.0)], initial_bankroll=100.0, base_stake=10.0
        )
