"""Per-team draw-streak staking simulation."""
from __future__ import annotations

from dataclasses import dataclass

from .staking import StakingResult, simulate_draw_progression


@dataclass(frozen=True, slots=True)
class TeamStakingReport:
    teams: int
    selected: int
    staking: StakingResult


def run_team_staking(
    selected_outcomes: dict[str, list[bool]],
    *,
    initial_bankroll: float = 1_000.0,
    base_stake: float = 10.0,
    payout_odds: float = 3.0,
) -> TeamStakingReport:
    bankroll = initial_bankroll
    all_bets = 0
    all_wins = 0
    max_drawdown = 0.0
    max_exposure = 0.0
    for team in sorted(selected_outcomes):
        result = simulate_draw_progression(
            selected_outcomes[team],
            initial_bankroll=bankroll,
            base_stake=base_stake,
            payout_odds=payout_odds,
        )
        bankroll = result.final_bankroll
        all_bets += result.bets
        all_wins += result.wins
        max_drawdown = max(max_drawdown, result.max_drawdown)
        max_exposure = max(max_exposure, result.max_exposure)
    return TeamStakingReport(
        teams=len(selected_outcomes),
        selected=sum(bool(values) for values in selected_outcomes.values()),
        staking=StakingResult(
            final_bankroll=bankroll,
            profit=bankroll - initial_bankroll,
            max_drawdown=max_drawdown,
            max_exposure=max_exposure,
            bets=all_bets,
            wins=all_wins,
        ),
    )
