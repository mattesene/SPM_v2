import pytest

from spm.backtest.odds_staking import simulate_draw_progression_with_odds


def test_bet_is_not_placed_when_required_stake_exceeds_bankroll():
    result = simulate_draw_progression_with_odds(
        [("A", False, 2.0), ("A", False, 2.0), ("A", False, 2.0)],
        initial_bankroll=25.0,
        base_stake=10.0,
    )
    assert result.bets == 2
    assert result.final_bankroll == pytest.approx(5.0)
    assert result.max_exposure == pytest.approx(20.0)


def test_max_exposure_tracks_concurrent_team_progressions():
    result = simulate_draw_progression_with_odds(
        [("A", False, 2.0), ("B", False, 2.0), ("A", False, 2.0)],
        initial_bankroll=100.0,
        base_stake=10.0,
    )
    assert result.max_exposure == pytest.approx(30.0)
