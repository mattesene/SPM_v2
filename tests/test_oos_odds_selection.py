from spm.backtest.odds_staking import OddsStakingResult
from spm.backtest.oos_odds_selection import rank_odds_staking_results


def test_odds_staking_results_are_ranked_and_limited_to_top_n():
    results = [
        (str(i), OddsStakingResult(100.0 + i, float(i), 1.0, 5.0, 10, 5, 0))
        for i in range(8)
    ]
    ranked = rank_odds_staking_results(results, initial_bankroll=100.0, min_bets=5)
    assert len(ranked) == 5
    assert [item.key for item in ranked] == ["7", "6", "5", "4", "3"]


def test_insufficient_oos_staking_results_are_excluded():
    results = [
        ("weak", OddsStakingResult(150.0, 50.0, 1.0, 5.0, 4, 4, 0)),
        ("valid", OddsStakingResult(120.0, 20.0, 2.0, 8.0, 6, 3, 0)),
    ]
    ranked = rank_odds_staking_results(results, initial_bankroll=100.0, min_bets=5)
    assert [item.key for item in ranked] == ["valid"]
