"""Public OOS pipeline entry points for odds-aware candidate selection."""
from __future__ import annotations

from collections.abc import Iterable
from datetime import date

from ..data.models import Match
from ..data.odds import DrawOdds
from .odds_staking import OddsStakingResult, simulate_draw_progression_with_odds
from .oos_dataset import build_team_staking_dataset
from .oos_odds_selection import rank_odds_staking_results
from .oos_selection import OOSCandidate
from .time_split import split_train_oos


def run_oos_odds_pipeline(
    datasets: Iterable[tuple[str, list[tuple[str, bool, float | None]]]],
    *,
    initial_bankroll: float,
    base_stake: float,
    min_bets: int = 5,
    limit: int = 5,
) -> tuple[OOSCandidate, ...]:
    """Simulate prepared OOS datasets and return their ranked Top-N."""
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


def run_oos_from_matches(
    matches: Iterable[Match],
    odds: Iterable[DrawOdds],
    *,
    initial_bankroll: float,
    base_stake: float,
    min_bets: int = 5,
    limit: int = 5,
) -> tuple[OOSCandidate, ...]:
    """Build team datasets from domain data and run the OOS ranking pipeline."""
    datasets = build_team_staking_dataset(matches, odds)
    return run_oos_odds_pipeline(
        datasets.items(),
        initial_bankroll=initial_bankroll,
        base_stake=base_stake,
        min_bets=min_bets,
        limit=limit,
    )


def run_oos_from_temporal_split(
    matches: Iterable[Match],
    odds: Iterable[DrawOdds],
    *,
    cutoff: date,
    initial_bankroll: float,
    base_stake: float,
    min_bets: int = 5,
    limit: int = 5,
) -> tuple[OOSCandidate, ...]:
    """Run ranking strictly on the OOS portion of a chronological split."""
    split = split_train_oos(list(matches), list(odds), cutoff)
    return run_oos_from_matches(
        split.oos,
        split.oos_odds,
        initial_bankroll=initial_bankroll,
        base_stake=base_stake,
        min_bets=min_bets,
        limit=limit,
    )
