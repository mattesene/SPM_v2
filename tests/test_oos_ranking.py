from spm.backtest.oos_ranking import rank_oos_results
from spm.backtest.oos_staking import OOSStakingWindowResult


def test_oos_ranking_prefers_risk_adjusted_performance():
    strong = OOSStakingWindowResult(None, 10, 10, 100.0, 1100.0, 10.0)
    weak = OOSStakingWindowResult(None, 10, 10, 80.0, 1080.0, 80.0)
    result = rank_oos_results(((weak, "B"), (strong, "A")), key_fn=lambda x: x)
    assert result[0].key == "A"
    assert result[0].bets == 10


def test_minimum_bet_filter():
    row = OOSStakingWindowResult(None, 2, 2, 20.0, 1020.0, 0.0)
    assert rank_oos_results(((row, "A"),), key_fn=lambda x: x, min_bets=3) == ()
