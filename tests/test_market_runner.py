from datetime import date

from spm.backtest.market_runner import _streaks_before_matches, run_market_backtest
from spm.data.models import Match
from spm.data.odds import DrawOdds


def test_market_runner_uses_only_selected_matches_and_market_prices():
    matches = [
        Match(date(2026, 1, 1), "A", "B", 1, 0),
        Match(date(2026, 1, 2), "A", "B", 0, 0),
        Match(date(2026, 1, 3), "A", "B", 0, 0),
        Match(date(2026, 1, 4), "A", "B", 0, 0),
    ]
    odds = [DrawOdds(date(2026, 1, 4), "A", "B", 3.5)]
    observations, staking = run_market_backtest(
        matches, odds, min_history=3, threshold=0.0, initial_bankroll=100.0, base_stake=10.0
    )
    assert len(observations) == 1
    assert observations[0].selected is True
    assert observations[0].draw_odds == 3.5
    assert observations[0].home_streak == 3
    assert staking.bets == 1
    assert staking.wins == 1
    assert staking.final_bankroll == 125.0


def test_market_runner_keeps_missing_price_explicit():
    matches = [
        Match(date(2026, 1, 1), "A", "B", 1, 0),
        Match(date(2026, 1, 2), "A", "B", 0, 0),
        Match(date(2026, 1, 3), "A", "B", 0, 0),
    ]
    observations, staking = run_market_backtest(
        matches, [], min_history=2, threshold=0.0, initial_bankroll=100.0, base_stake=10.0
    )
    assert observations[0].draw_odds is None
    assert staking.bets == 0
    assert staking.skipped == 0


def test_streaks_include_warmup_matches_and_reset_after_draw():
    matches = [
        Match(date(2024, 1, 1), "Inter", "Milan", 1, 0),
        Match(date(2024, 1, 8), "Roma", "Inter", 2, 0),
        Match(date(2024, 1, 15), "Inter", "Napoli", 1, 1),
        Match(date(2024, 1, 22), "Milan", "Inter", 0, 1),
    ]
    streaks = _streaks_before_matches(matches)
    assert streaks[matches[0]] == (0, 0)
    assert streaks[matches[1]] == (0, 1)
    assert streaks[matches[2]] == (2, 0)
    assert streaks[matches[3]] == (0, 0)
