"""Quality gates for acquired Live fixtures."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from spm.data.fixtures import Fixture


@dataclass(frozen=True)
class FixtureQuality:
    accepted: list[Fixture]
    rejected: int
    duplicates_removed: int


def quality_gate(fixtures: list[Fixture]) -> FixtureQuality:
    accepted: list[Fixture] = []
    seen: set[tuple[str, str, date]] = set()
    rejected = 0
    duplicates = 0
    for fixture in fixtures:
        home = " ".join(fixture.home.strip().split())
        away = " ".join(fixture.away.strip().split())
        if not home or not away or home == away:
            rejected += 1
            continue
        normalized = Fixture(home, away, fixture.kickoff)
        key = (normalized.home, normalized.away, normalized.kickoff)
        if key in seen:
            duplicates += 1
            continue
        seen.add(key)
        accepted.append(normalized)
    return FixtureQuality(accepted, rejected, duplicates)
