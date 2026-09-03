"""Adapters from played matches and draw odds to staking datasets."""
from __future__ import annotations

from collections.abc import Iterable

from ..data.models import Match
from ..data.odds import DrawOdds, index_draw_odds
from ..data.normalization import canonical_team_name


def build_team_staking_dataset(matches: Iterable[Match], odds: Iterable[DrawOdds]) -> dict[str, list[tuple[str, bool, float | None]]]:
    """Build per-team chronological staking selections from match/odds data."""
    odds_index = index_draw_odds(list(odds))
    datasets: dict[str, list[tuple[str, bool, float | None]]] = {}
    ordered = sorted(matches, key=lambda item: item.date)
    for match in ordered:
        key = (match.date, canonical_team_name(match.home_team), canonical_team_name(match.away_team))
        draw_odds = odds_index.get(key)
        datasets.setdefault(match.home_team, []).append((match.home_team, match.is_draw, draw_odds))
        datasets.setdefault(match.away_team, []).append((match.away_team, match.is_draw, draw_odds))
    return datasets
