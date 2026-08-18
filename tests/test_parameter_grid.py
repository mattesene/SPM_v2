from spm.backtest.parameter_grid import StakingConfig, build_staking_grid


def test_build_staking_grid_is_deterministic_and_filters_invalid_values():
    result = build_staking_grid([1000.0], [10.0, 20.0], [2.0, 3.0])
    assert result == [
        StakingConfig(1000.0, 10.0, 2.0),
        StakingConfig(1000.0, 10.0, 3.0),
        StakingConfig(1000.0, 20.0, 2.0),
        StakingConfig(1000.0, 20.0, 3.0),
    ]
