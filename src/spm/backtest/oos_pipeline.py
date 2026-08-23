"""Public OOS pipeline entry point for odds-aware candidate selection."""
from __future__ import annotations

from collections.abc import Iterable

from .odds_staking import OddsStakingResult, simulate_draw_progression_with_odds
from .oos_odds_selection import rank_odds_staking_results
from .oos_selection import OOSCandidate


def run_oos_odds_pipeline(
    datasets: Iterable[tuple[str, list[tuple[str, bool, float | None]]]],
    *,
    initial_bankroll: float,
    base_stake: float,
    min_bets: int = 5,
    limit: int = 5,
) -> tuple[OOSCandidate, ...]:
    """Simulate each OOS dataset and return its ranked Top-N candidates."""
    results: list[tuple[str, OddsStakingResult]] = []
    for key, selections in datasets:
        result = simulate_draw_progression_with_odds(
            selections,
            initial_bankroll=initial_bankroll,
            base_stake=base_stake,
        )
        results.append((key, result))
    return rank_odds_staking_results(
        results,
        initial_bankroll=initial_bankroll,
        min_bets=min_bets,
        limit=limit,
    )
