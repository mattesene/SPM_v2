"""Adapter applying canonical team normalization to historical matches."""
from __future__ import annotations

from dataclasses import replace
from typing import Iterable

from .normalization import canonical_team_name
from .schema import HistoricalMatch


def canonicalize_matches(matches: Iterable[HistoricalMatch]) -> tuple[HistoricalMatch, ...]:
    """Return matches with provider-specific team names mapped to canonical keys."""
    output = []
    for match in matches:
        output.append(
            replace(
                match,
                home_team=canonical_team_name(match.home_team),
                away_team=canonical_team_name(match.away_team),
            )
        )
    return tuple(output)
