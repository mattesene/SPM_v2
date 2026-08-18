from spm.backtest.parameter_grid import StakingConfig
from spm.backtest.walk_forward import run_walk_forward


def test_backtest_walk_forward_keeps_validation_out_of_sample():
    configs = [StakingConfig(1000.0, 10.0, 2.0), StakingConfig(1000.0, 20.0, 2.0)]
    result = run_walk_forward([False, True, False, True], configs, train_size=2)
    assert result.selected in configs
    assert result.validation.staking.bets > 0
