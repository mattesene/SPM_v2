"""Bridge odds-aware OOS staking results into the Top-N selector."""
from __future__ import annotations

from collections.abc import Iterable

from .odds_staking import OddsStakingResult
from .oos_selection import OOSCandidate, build_oos_candidate, select_top_oos_candidates


def rank_odds_staking_results(
    results: Iterable[tuple[str, OddsStakingResult]],
    *,
    initial_bankroll: float,
    min_bets: int = 5,
    limit: int = 5,
) -> tuple[OOSCandidate, ...]:
    """Convert completed odds-aware OOS simulations into ranked candidates."""
    candidates = (
        build_oos_candidate(
            key,
            bets=result.bets,
            wins=result.wins,
            profit=result.profit,
            max_drawdown=result.max_drawdown,
            max_exposure=result.max_exposure,
            initial_bankroll=initial_bankroll,
        )
        for key, result in results
    )
    return select_top_oos_candidates(candidates, min_bets=min_bets, limit=limit)
