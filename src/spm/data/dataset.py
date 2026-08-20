"""Deterministic join of match results and draw-market odds."""
from __future__ import annotations

from dataclasses import dataclass
from .odds import DrawOdds
from .results import MatchResult


@dataclass(frozen=True, slots=True)
class MatchWithOdds:
    result: MatchResult
    odds: DrawOdds


def join_results_and_odds(results: tuple[MatchResult, ...], odds: tuple[DrawOdds, ...]) -> tuple[MatchWithOdds, ...]:
    """Join on date/home/away and reject missing or conflicting records."""
    index: dict[tuple[object, str, str], DrawOdds] = {}
    for quote in odds:
        key = (quote.match_date, quote.home_team.strip().casefold(), quote.away_team.strip().casefold())
        if key in index and index[key].draw_odds != quote.draw_odds:
            raise ValueError(f"conflicting odds for {key}")
        index[key] = quote

    joined: list[MatchWithOdds] = []
    missing: list[tuple[object, str, str]] = []
    for result in results:
        key = (result.match_date, result.home_team.strip().casefold(), result.away_team.strip().casefold())
        quote = index.get(key)
        if quote is None:
            missing.append(key)
            continue
        joined.append(MatchWithOdds(result, quote))
    if missing:
        raise ValueError(f"missing odds for {len(missing)} matches")
    return tuple(joined)
