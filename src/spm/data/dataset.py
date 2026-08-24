"""Deterministic join of match results and draw-market odds."""
from __future__ import annotations

from dataclasses import dataclass
from .normalization import canonical_team_name
from .odds import DrawOdds, index_draw_odds
from .results import MatchResult


@dataclass(frozen=True, slots=True)
class MatchWithOdds:
    result: MatchResult
    odds: DrawOdds


def join_results_and_odds(results: tuple[MatchResult, ...], odds: tuple[DrawOdds, ...]) -> tuple[MatchWithOdds, ...]:
    """Join on canonical date/home/away and reject missing or conflicting records."""
    index_draw_odds(list(odds))
    by_key = {q.identity_key: q for q in odds}
    joined: list[MatchWithOdds] = []
    missing: list[tuple[object, str, str]] = []
    for result in results:
        key = (
            result.match_date,
            canonical_team_name(result.home_team),
            canonical_team_name(result.away_team),
        )
        quote = by_key.get(key)
        if quote is None:
            missing.append(key)
            continue
        joined.append(MatchWithOdds(result, quote))
    if missing:
        raise ValueError(f"missing odds for {len(missing)} matches")
    return tuple(joined)
