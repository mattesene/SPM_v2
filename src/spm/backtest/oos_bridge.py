"""Adapters that turn OOS window results into live-ranking evidence."""
from __future__ import annotations

from collections.abc import Callable, Iterable

from .oos_ranking import OOSRankingEntry, rank_oos_results
from .oos_staking import OOSStakingWindowResult


def build_oos_entries(
    rows: Iterable[tuple[OOSStakingWindowResult, object]],
    *,
    key_fn: Callable[[object], object],
    initial_bankroll: float = 1_000.0,
    min_bets: int = 1,
) -> tuple[OOSRankingEntry, ...]:
    """Create the canonical OOS evidence consumed by live selection."""
    return rank_oos_results(
        rows,
        key_fn=key_fn,
        initial_bankroll=initial_bankroll,
        min_bets=min_bets,
    )
