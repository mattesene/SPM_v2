"""Walk-forward parameter selection to limit in-sample overfitting."""
from __future__ import annotations

from dataclasses import dataclass

from spm.backtest.parameter_search import ParameterResult, evaluate_grid, rank_by_profit
from spm.backtest.parameter_grid import StakingConfig


@dataclass(frozen=True, slots=True)
class WalkForwardResult:
    selected: StakingConfig
    validation: ParameterResult


def run_walk_forward(
    outcomes: list[bool],
    configs: list[StakingConfig],
    train_size: int,
) -> WalkForwardResult:
    if train_size <= 0 or train_size >= len(outcomes):
        raise ValueError("train_size must split the observations")
    train = outcomes[:train_size]
    validation = outcomes[train_size:]
    ranked = rank_by_profit(evaluate_grid(train, configs))
    selected = ranked[0].config
    validated = evaluate_grid(validation, [selected])[0]
    return WalkForwardResult(selected, validated)
