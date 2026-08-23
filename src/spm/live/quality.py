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
        if not fixture.home.strip() or not fixture.away.strip() or fixture.home == fixture.away:
            rejected += 1
            continue
        key = (fixture.home, fixture.away, fixture.kickoff)
        if key in seen:
            duplicates += 1
            continue
        seen.add(key)
        accepted.append(fixture)
    return FixtureQuality(accepted, rejected, duplicates)
