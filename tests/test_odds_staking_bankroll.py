from spm.backtest.odds_staking import simulate_draw_progression_with_odds


def test_bankroll_insufficient_stake_is_not_counted_as_bet():
    result = simulate_draw_progression_with_odds(
        [("A", False, 2.0), ("A", False, 2.0), ("A", True, 3.0)],
        initial_bankroll=15.0,
        base_stake=10.0,
    )
    assert result.bets == 1
    assert result.wins == 0
    assert result.final_bankroll == 5.0


def test_insufficient_bankroll_does_not_change_stake_progression():
    result = simulate_draw_progression_with_odds(
        [("A", False, 2.0), ("A", False, 2.0)],
        initial_bankroll=15.0,
        base_stake=10.0,
    )
    assert result.bets == 1
    assert result.skipped == 0
    assert result.final_bankroll == 5.0
