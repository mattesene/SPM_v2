"""Chronological train/OOS splitting with an explicit leakage-safe boundary."""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date

from ..data.models import Match
from ..data.odds import DrawOdds


@dataclass(frozen=True, slots=True)
class TemporalSplit:
    train: tuple[Match, ...]
    oos: tuple[Match, ...]
    train_odds: tuple[DrawOdds, ...]
    oos_odds: tuple[DrawOdds, ...]
    cutoff: date


def split_train_oos(
    matches: Sequence[Match], odds: Sequence[DrawOdds], cutoff: date
) -> TemporalSplit:
    """Split matches and odds using the same chronological boundary."""
    ordered_matches = tuple(sorted(matches, key=lambda item: item.date))
    ordered_odds = tuple(sorted(odds, key=lambda item: item.date))
    return TemporalSplit(
        train=tuple(item for item in ordered_matches if item.date < cutoff),
        oos=tuple(item for item in ordered_matches if item.date >= cutoff),
        train_odds=tuple(item for item in ordered_odds if item.date < cutoff),
        oos_odds=tuple(item for item in ordered_odds if item.date >= cutoff),
        cutoff=cutoff,
    )
