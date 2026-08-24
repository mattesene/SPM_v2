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
    selections: list[tuple[str, bool, float | None]],
    *,
    initial_bankroll: float,
    base_stake: float,
) -> OddsStakingResult:
    """Simulate independent draw progressions for each selected team.

    ``selections`` contains ``(team, actual_draw, decimal_draw_odds)`` in
    chronological order. A loss doubles the *same team's* next stake; a draw
    resets only that team's progression. Missing prices skip the match without
    changing that team's progression. This mirrors the SPM rule of continuing
    the draw progression on the same team rather than carrying one global
    martingale across unrelated teams.
    """
    if initial_bankroll < 0 or base_stake <= 0:
        raise ValueError("invalid bankroll or stake")
    bankroll = initial_bankroll
    peak = bankroll
    max_drawdown = 0.0
    max_exposure = 0.0
    stakes: dict[str, float] = {}
    exposure_by_team: dict[str, float] = {}
    bets = wins = skipped = 0

    for team, is_draw, odds in selections:
        if odds is None:
            skipped += 1
            continue
        if odds <= 1.0:
            raise ValueError("odds must be greater than 1.0")
        stake = stakes.get(team, base_stake)
        if stake > bankroll:
            continue
        bankroll -= stake
        exposure_by_team[team] = stake
        max_exposure = max(max_exposure, sum(exposure_by_team.values()))
        bets += 1
        if is_draw:
            bankroll += stake * odds
            wins += 1
            stakes[team] = base_stake
            exposure_by_team.pop(team, None)
        else:
            stakes[team] = stake * 2.0
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
