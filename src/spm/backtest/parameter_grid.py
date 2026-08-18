"""Deterministic parameter-grid utilities for SPM backtest experiments."""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product


@dataclass(frozen=True, slots=True)
class StakingConfig:
    initial_bankroll: float
    base_stake: float
    payout_odds: float


def build_staking_grid(
    bankrolls: list[float],
    base_stakes: list[float],
    payout_odds: list[float],
) -> list[StakingConfig]:
    configs = [StakingConfig(*values) for values in product(bankrolls, base_stakes, payout_odds)]
    return [c for c in configs if c.initial_bankroll >= 0 and c.base_stake > 0 and c.payout_odds > 0]
