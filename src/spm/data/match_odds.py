"""Strict matching of historical matches and draw odds."""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Sequence

from .models import Match
from .odds import DrawOdds


@dataclass(frozen=True, slots=True)
class MatchedMatchOdds:
    match: Match
    draw_odds: float


def attach_draw_odds(matches: Sequence[Match], odds: Sequence[DrawOdds]) -> tuple[MatchedMatchOdds, ...]:
    index: dict[tuple[object, str, str], list[float]] = defaultdict(list)
    for item in odds:
        index[(item.date, item.home_team, item.away_team)].append(item.draw_odds)

    result: list[MatchedMatchOdds] = []
    for match in matches:
        prices = index.get((match.date, match.home_team, match.away_team), [])
        if len(prices) > 1 and len(set(prices)) > 1:
            raise ValueError(f"ambiguous draw odds for {match.date} {match.home_team}-{match.away_team}")
        if len(prices) == 1:
            result.append(MatchedMatchOdds(match, prices[0]))
    return tuple(result)
