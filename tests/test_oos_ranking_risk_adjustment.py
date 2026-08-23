from dataclasses import replace

from spm.backtest.oos_ranking import rank_oos_results
from spm.backtest.oos_staking import OOSStakingWindowResult


def test_oos_ranking_penalizes_drawdown():
    low_risk = OOSStakingWindowResult(None, 10, 10, 80.0, 1080.0, 10.0)
    high_risk = OOSStakingWindowResult(None, 10, 10, 90.0, 1090.0, 200.0)
    rows = [(low_risk, "low"), (high_risk, "high")]
    ranked = rank_oos_results(rows, key_fn=lambda value: value, initial_bankroll=1000.0, min_bets=1)
    assert ranked[0].key == "low"
    assert ranked[0].max_drawdown == 10.0
    assert ranked[1].max_drawdown == 200.0
