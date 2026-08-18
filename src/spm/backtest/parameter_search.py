"""Evaluate staking configurations without selecting on the same sample."""
from __future__ import annotations

from dataclasses import dataclass

from spm.backtest.parameter_grid import StakingConfig, build_staking_grid
from spm.backtest.staking import StakingResult, simulate_draw_progression


@dataclass(frozen=True, slots=True)
class ParameterResult:
    config: StakingConfig
    staking: StakingResult


def evaluate_grid(outcomes: list[bool], configs: list[StakingConfig]) -> list[ParameterResult]:
    return [
        ParameterResult(
            config,
            simulate_draw_progression(
                outcomes,
                initial_bankroll=config.initial_bankroll,
                base_stake=config.base_stake,
                payout_odds=config.payout_odds,
            ),
        )
        for config in configs
    ]


def rank_by_profit(results: list[ParameterResult]) -> list[ParameterResult]:
    return sorted(results, key=lambda item: item.staking.profit, reverse=True)
