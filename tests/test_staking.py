import pytest

from spm.backtest.staking import simulate_draw_progression


def test_draw_resets_stake_and_records_profit():
    result = simulate_draw_progression([False, True], 100.0, 10.0, 2.0)
    assert result.bets == 2
    assert result.wins == 1
    assert result.final_bankroll == pytest.approx(110.0)
    assert result.max_exposure == pytest.approx(30.0)


def test_progression_stops_when_bankroll_cannot_cover_next_stake():
    result = simulate_draw_progression([False, False, False], 25.0, 10.0, 2.0)
    assert result.bets == 2
    assert result.final_bankroll == pytest.approx(5.0)
