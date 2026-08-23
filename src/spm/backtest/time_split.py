"""Chronological train/OOS splitting with an explicit leakage-safe boundary."""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date

from ..data.models import Match


@dataclass(frozen=True, slots=True)
class TemporalSplit:
    train: tuple[Match, ...]
    oos: tuple[Match, ...]
    cutoff: date


def split_train_oos(matches: Sequence[Match], cutoff: date) -> TemporalSplit:
    """Split chronologically: train strictly before cutoff, OOS on/after cutoff."""
    ordered = tuple(sorted(matches, key=lambda item: item.date))
    train = tuple(item for item in ordered if item.date < cutoff)
    oos = tuple(item for item in ordered if item.date >= cutoff)
    return TemporalSplit(train=train, oos=oos, cutoff=cutoff)
