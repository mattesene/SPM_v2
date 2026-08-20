"""Deterministic join of match results and draw-market odds."""
from __future__ import annotations

from dataclasses import dataclass
from .odds import DrawOdds, index_draw_odds
from .results import MatchResult


@dataclass(frozen=True, slots=True)
class MatchWithOdds:
    result: MatchResult
    odds: DrawOdds


def join_results_and_odds(results: tuple[MatchResult, ...], odds: tuple[DrawOdds, ...]) -> tuple[MatchWithOdds, ...]:
    """Join on date/home/away and reject missing or conflicting records."""
    index = index_draw_odds(list(odds))
    joined: list[MatchWithOdds] = []
    missing: list[tuple[object, str, str]] = []
    for result in results:
        key = (result.match_date, result.home_team.strip().casefold(), result.away_team.strip().casefold())
        quote = next((q for q in odds if q.identity_key == key), None)
        if quote is None:
            missing.append(key)
            continue
        joined.append(MatchWithOdds(result, quote))
    if missing:
        raise ValueError(f"missing odds for {len(missing)} matches")
    return tuple(joined)
