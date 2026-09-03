"""Build SPM scores for persisted upcoming fixtures."""
from __future__ import annotations

from datetime import date
from typing import Iterable

from spm.data.fixtures import Fixture
from spm.data.models import Match
from spm.statistics.engine import SPMEngine, SPMScore


def score_fixtures(
    matches: list[Match],
    fixtures: Iterable[Fixture],
    *,
    as_of: date,
    engine: SPMEngine | None = None,
) -> tuple[SPMScore, ...]:
    """Score upcoming fixtures, skipping fixtures without historical coverage."""
    scorer = engine or SPMEngine()
    fixture_rows = tuple(fixtures)
    upcoming = sorted(
        (fixture for fixture in fixture_rows if fixture.date >= as_of),
        key=lambda item: item.date,
    )
    print(
        "live_scoring,"
        f"matches={len(matches)},fixtures_in={len(fixture_rows)},fixtures_upcoming={len(upcoming)},"
        f"as_of={as_of.isoformat()},dates={[fixture.date.isoformat() for fixture in upcoming]}",
        flush=True,
    )

    scored: list[SPMScore] = []
    skipped: list[tuple[str, str, str]] = []
    for fixture in upcoming:
        try:
            scored.append(scorer.score(matches, fixture.home_team, fixture.away_team, as_of))
        except ValueError as exc:
            # Live feeds can use localized/new team names that are not present
            # in the historical corpus. One unmapped fixture must not suppress
            # valid predictions for the other fixtures.
            if "historical match" not in str(exc):
                raise
            skipped.append((fixture.home_team, fixture.away_team, str(exc)))

    if skipped:
        print(f"live_scoring,skipped={skipped}", flush=True)
    print(f"live_scoring,scores={len(scored)}", flush=True)
    return tuple(scored)
