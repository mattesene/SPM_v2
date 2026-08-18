"""Bankroll simulation for the SPM draw progression."""
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class StakingResult:
    final_bankroll: float
    profit: float
    max_drawdown: float
    max_exposure: float
    bets: int
    wins: int


def simulate_draw_progression(
    outcomes: list[bool],
    initial_bankroll: float,
    base_stake: float,
    payout_odds: float,
) -> StakingResult:
    if initial_bankroll < 0 or base_stake <= 0 or payout_odds <= 0:
        raise ValueError("invalid bankroll, stake or odds")
    bankroll = initial_bankroll
    peak = bankroll
    max_drawdown = 0.0
    exposure = 0.0
    max_exposure = 0.0
    stake = base_stake
    bets = wins = 0
    for is_draw in outcomes:
        if stake > bankroll:
            break
        bankroll -= stake
        exposure += stake
        max_exposure = max(max_exposure, exposure)
        bets += 1
        if is_draw:
            bankroll += stake * payout_odds
            wins += 1
            stake = base_stake
            exposure = 0.0
        else:
            stake *= 2.0
        peak = max(peak, bankroll)
        max_drawdown = max(max_drawdown, peak - bankroll)
    return StakingResult(bankroll, bankroll - initial_bankroll, max_drawdown, max_exposure, bets, wins)
