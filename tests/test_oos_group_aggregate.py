from spm.backtest.oos_group_aggregate import aggregate_oos_by_group
from spm.backtest.oos_staking import OOSStakingWindowResult


def test_grouped_oos_aggregation():
    a = OOSStakingWindowResult(None, 2, 2, 20.0, 1020.0, 0.0)
    b = OOSStakingWindowResult(None, 1, 1, -5.0, 995.0, 5.0)
    result = aggregate_oos_by_group(((a, "SerieA"), (b, "SerieA")), key_fn=lambda x: x)
    assert len(result) == 1
    assert result[0].key == "SerieA"
    assert result[0].bets == 3
    assert result[0].profit == 15.0
    assert result[0].profitable_windows == 1
