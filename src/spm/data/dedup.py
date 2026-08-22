"""Deterministic match deduplication across data providers."""
from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from .models import Match
from .normalize import normalize_team_name


@dataclass(frozen=True, slots=True)
class DuplicateGroup:
    key: tuple[object, str, str]
    matches: tuple[Match, ...]


def match_key(match: Match) -> tuple[object, str, str]:
    """Build a provider-independent identity key for a played fixture."""
    home = normalize_team_name(match.home_team)
    away = normalize_team_name(match.away_team)
    return match.date, home, away


def group_duplicates(matches: Iterable[Match]) -> tuple[DuplicateGroup, ...]:
    groups: dict[tuple[object, str, str], list[Match]] = {}
    for match in matches:
        groups.setdefault(match_key(match), []).append(match)
    return tuple(
        DuplicateGroup(key, tuple(rows))
        for key, rows in groups.items()
        if len(rows) > 1
    )


def deduplicate_matches(matches: Iterable[Match]) -> list[Match]:
    """Keep the first occurrence of an identical fixture while preserving order."""
    seen: set[tuple[object, str, str]] = set()
    result: list[Match] = []
    for match in matches:
        key = match_key(match)
        if key not in seen:
            seen.add(key)
            result.append(match)
    return result
