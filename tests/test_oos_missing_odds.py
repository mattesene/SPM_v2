from spm.backtest.odds_staking import simulate_draw_progression_with_odds


def test_missing_odds_do_not_count_as_bets():
    result = simulate_draw_progression_with_odds(
        [("A", True, None), ("A", False, 2.0), ("A", True, None)],
        initial_bankroll=100.0,
        base_stake=10.0,
    )
    assert result.skipped == 2
    assert result.bets == 1
    assert result.wins == 0


def test_missing_odds_do_not_advance_progression():
    result = simulate_draw_progression_with_odds(
        [("A", False, None), ("A", False, 2.0), ("A", True, 3.0)],
        initial_bankroll=100.0,
        base_stake=10.0,
    )
    assert result.bets == 2
    assert result.skipped == 1
    # First playable bet is 10; after the loss the next playable bet is 20.
    assert result.final_bankroll == 130.0
