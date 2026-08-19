from spm.backtest.oos_aggregate import aggregate_oos_staking
from spm.backtest.oos_staking import OOSStakingWindowResult


def test_aggregate_oos_results():
    rows = (
        OOSStakingWindowResult(None, 2, 2, 20.0, 1020.0, 0.0),
        OOSStakingWindowResult(None, 1, 1, -5.0, 995.0, 5.0),
    )
    result = aggregate_oos_staking(rows, initial_bankroll=1000.0)
    assert result.windows == 2
    assert result.bets == 3
    assert result.profit == 15.0
    assert result.final_bankroll == 1015.0
    assert result.roi == .015
    assert result.max_drawdown == 0.0
    assert result.winning_windows == 1
