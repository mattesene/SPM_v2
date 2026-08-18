"""Connect SPM selection outcomes to bankroll simulation."""
from dataclasses import dataclass

from spm.backtest.staking import StakingResult, simulate_draw_progression


@dataclass(frozen=True, slots=True)
class StakingBacktestReport:
    staking: StakingResult
    draw_rate: float
    observations: int


def run_staking_backtest(
    outcomes: list[bool],
    initial_bankroll: float = 1_000.0,
    base_stake: float = 10.0,
    payout_odds: float = 3.0,
) -> StakingBacktestReport:
    result = simulate_draw_progression(
        outcomes,
        initial_bankroll=initial_bankroll,
        base_stake=base_stake,
        payout_odds=payout_odds,
    )
    rate = sum(outcomes) / len(outcomes) if outcomes else 0.0
    return StakingBacktestReport(result, rate, len(outcomes))
