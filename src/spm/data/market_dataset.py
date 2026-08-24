"""Build canonical backtest observations from normalized matches and draw odds."""
from __future__ import annotations

from dataclasses import dataclass

from .normalized import MatchRecord
from .odds import DrawOdds, index_draw_odds


@dataclass(frozen=True, slots=True)
class MarketMatch:
    match: MatchRecord
    draw_odds: float


def attach_draw_odds(
    matches: list[MatchRecord], odds: list[DrawOdds]
) -> tuple[MarketMatch, ...]:
    index = index_draw_odds(odds)
    attached: list[MarketMatch] = []
    missing = 0
    for match in matches:
        key = match.identity_key[:3]
        price = index.get(key)
        if price is None:
            missing += 1
            continue
        attached.append(MarketMatch(match, price))
    if missing:
        raise ValueError(f"missing draw odds for {missing} matches")
    return tuple(attached)
