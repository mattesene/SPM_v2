"""Progressive staking engine for the SPM draw strategy."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class StakeStep:
    stake: float
    outcome: str
    profit: float
    next_stake: float


def apply_stake(bankroll: float, stake: float, odds: float, outcome: str) -> StakeStep:
    if bankroll < 0 or stake <= 0 or stake > bankroll:
        raise ValueError("stake must be positive and no greater than bankroll")
    if odds <= 1:
        raise ValueError("odds must be greater than 1")
    if outcome not in {"draw", "non_draw"}:
        raise ValueError("outcome must be draw or non_draw")
    if outcome == "draw":
        profit = stake * (odds - 1)
        next_stake = stake
    else:
        profit = -stake
        next_stake = stake * 2
    return StakeStep(stake, outcome, profit, next_stake)
