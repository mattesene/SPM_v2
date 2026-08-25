"""Quality gates for acquired Live fixtures."""
from __future__ import annotations

from dataclasses import dataclass

from spm.data.fixtures import Fixture


@dataclass(frozen=True)
class FixtureQuality:
    accepted: list[Fixture]
    rejected: int
    duplicates_removed: int


def quality_gate(fixtures: list[Fixture]) -> FixtureQuality:
    accepted: list[Fixture] = []
    seen: set[tuple[str, str, object]] = set()
    rejected = 0
    duplicates = 0
    for fixture in fixtures:
        home = " ".join(fixture.home_team.strip().split())
        away = " ".join(fixture.away_team.strip().split())
        if not home or not away or home.casefold() == away.casefold():
            rejected += 1
            continue
        normalized = Fixture(home, away, fixture.date)
        key = (normalized.home_team.casefold(), normalized.away_team.casefold(), normalized.date)
        if key in seen:
            duplicates += 1
            continue
        seen.add(key)
        accepted.append(normalized)
    return FixtureQuality(accepted, rejected, duplicates)
