"""Apply the SPM staking progression to catalog backtest outcomes."""
from __future__ import annotations

from dataclasses import dataclass

from .staking import StakingResult, simulate_draw_progression


@dataclass(frozen=True, slots=True)
class CatalogStakingResult:
    datasets: int
    observations: int
    draw_rate: float
    staking: StakingResult


def run_catalog_staking(
    outcomes_by_dataset: dict[str, list[bool]],
    *,
    initial_bankroll: float = 1_000.0,
    base_stake: float = 10.0,
    payout_odds: float = 3.0,
) -> CatalogStakingResult:
    outcomes: list[bool] = []
    for dataset in sorted(outcomes_by_dataset):
        outcomes.extend(outcomes_by_dataset[dataset])
    observations = len(outcomes)
    draw_rate = sum(outcomes) / observations if observations else 0.0
    staking = simulate_draw_progression(
        outcomes,
        initial_bankroll=initial_bankroll,
        base_stake=base_stake,
        payout_odds=payout_odds,
    )
    return CatalogStakingResult(
        datasets=len(outcomes_by_dataset),
        observations=observations,
        draw_rate=draw_rate,
        staking=staking,
    )
