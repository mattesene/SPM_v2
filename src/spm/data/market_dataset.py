"""Build canonical backtest observations from normalized matches and draw odds."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from .normalized import MatchRecord
from .odds import DrawOdds


@dataclass(frozen=True, slots=True)
class MarketMatch:
    match: MatchRecord
    draw_odds: float


def attach_draw_odds(
    matches: list[MatchRecord], odds: list[DrawOdds]
) -> tuple[MarketMatch, ...]:
    index: dict[tuple[date, str, str], float] = {}
    for quote in odds:
        key = (
            quote.match_date,
            quote.home_team.strip().casefold(),
            quote.away_team.strip().casefold(),
        )
        previous = index.get(key)
        if previous is not None and previous != quote.draw_odds:
            raise ValueError(f"conflicting draw odds for {key}")
        index[key] = quote.draw_odds

    attached: list[MarketMatch] = []
    missing = 0
    for match in matches:
        key = (
            match.date,
            match.canonical_home_team,
            match.canonical_away_team,
        )
        price = index.get(key)
        if price is None:
            missing += 1
            continue
        attached.append(MarketMatch(match, price))

    if missing:
        raise ValueError(f"missing draw odds for {missing} matches")
    return tuple(attached)
