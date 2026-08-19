"""Odds-aware staking simulation for historical draw selections."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OddsStakingResult:
    final_bankroll: float
    profit: float
    max_drawdown: float
    max_exposure: float
    bets: int
    wins: int
    skipped: int


def simulate_draw_progression_with_odds(
    selections: list[tuple[bool, float | None]],
    *,
    initial_bankroll: float,
    base_stake: float,
) -> OddsStakingResult:
    """Simulate the SPM draw progression using the odds available per match.

    A missing price skips the match without changing the progression. A
    non-draw doubles the next stake; a draw resets it to the base stake.
    Winnings are settled at decimal odds, so the returned stake is stake*odds.
    """
    if initial_bankroll < 0 or base_stake <= 0:
        raise ValueError("invalid bankroll or stake")
    bankroll = initial_bankroll
    peak = bankroll
    max_drawdown = 0.0
    exposure = 0.0
    max_exposure = 0.0
    stake = base_stake
    bets = wins = skipped = 0

    for is_draw, odds in selections:
        if odds is None:
            skipped += 1
            continue
        if odds <= 1.0:
            raise ValueError("odds must be greater than 1.0")
        if stake > bankroll:
            break
        bankroll -= stake
        exposure += stake
        max_exposure = max(max_exposure, exposure)
        bets += 1
        if is_draw:
            bankroll += stake * odds
            wins += 1
            stake = base_stake
            exposure = 0.0
        else:
            stake *= 2.0
        peak = max(peak, bankroll)
        max_drawdown = max(max_drawdown, peak - bankroll)

    return OddsStakingResult(
        final_bankroll=bankroll,
        profit=bankroll - initial_bankroll,
        max_drawdown=max_drawdown,
        max_exposure=max_exposure,
        bets=bets,
        wins=wins,
        skipped=skipped,
    )
