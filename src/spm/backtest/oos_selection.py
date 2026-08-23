"""Out-of-sample candidate ranking and Top-N selection."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence


@dataclass(frozen=True, slots=True)
class OOSCandidate:
    key: str
    bets: int
    wins: int
    profit: float
    roi: float
    max_drawdown: float
    max_exposure: float
    score: float


def build_oos_candidate(
    key: str,
    *,
    bets: int,
    wins: int,
    profit: float,
    max_drawdown: float,
    max_exposure: float,
    initial_bankroll: float,
) -> OOSCandidate:
    if not key.strip():
        raise ValueError("candidate key cannot be empty")
    if initial_bankroll <= 0:
        raise ValueError("initial_bankroll must be positive")
    if bets < 0 or wins < 0 or wins > bets:
        raise ValueError("invalid bet/win counts")
    if max_drawdown < 0 or max_exposure < 0:
        raise ValueError("risk metrics cannot be negative")
    roi = profit / initial_bankroll
    # Reward return and hit rate, while penalising drawdown and exposure.
    score = roi + (wins / bets if bets else 0.0) * 0.10 - (max_drawdown / initial_bankroll) * 0.25 - (max_exposure / initial_bankroll) * 0.05
    return OOSCandidate(key, bets, wins, profit, roi, max_drawdown, max_exposure, score)


def select_top_oos_candidates(
    candidates: Iterable[OOSCandidate],
    *,
    min_bets: int = 5,
    limit: int = 5,
) -> tuple[OOSCandidate, ...]:
    if min_bets < 1:
        raise ValueError("min_bets must be positive")
    if limit < 1:
        raise ValueError("limit must be positive")
    unique: dict[str, OOSCandidate] = {}
    for candidate in candidates:
        if candidate.bets < min_bets:
            continue
        previous = unique.get(candidate.key)
        if previous is None or candidate.score > previous.score:
            unique[candidate.key] = candidate
    return tuple(sorted(unique.values(), key=lambda item: (-item.score, item.key))[:limit])
