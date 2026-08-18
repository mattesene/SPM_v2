from spm.backtest.parameter_grid import StakingConfig
from spm.backtest.parameter_search import evaluate_grid, rank_by_profit


def test_parameter_grid_results_are_ranked_by_profit():
    configs = [StakingConfig(1000.0, 10.0, 2.0), StakingConfig(1000.0, 20.0, 2.0)]
    ranked = rank_by_profit(evaluate_grid([False, True], configs))
    assert ranked[0].config.base_stake == 20.0
