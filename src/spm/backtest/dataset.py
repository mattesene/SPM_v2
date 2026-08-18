"""Utilities for building isolated competition/season backtest datasets."""
from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable

from spm.data.normalized import MatchRecord


def group_by_competition_season(
    records: Iterable[MatchRecord],
) -> dict[tuple[str, str], tuple[MatchRecord, ...]]:
    """Group normalized records without mixing competitions or seasons."""
    groups: dict[tuple[str, str], list[MatchRecord]] = defaultdict(list)
    for record in records:
        key = (record.competition or "unknown", record.season or "unknown")
        groups[key].append(record)
    return {key: tuple(sorted(value, key=lambda item: item.date)) for key, value in groups.items()}
