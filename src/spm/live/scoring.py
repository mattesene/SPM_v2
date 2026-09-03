"""Build SPM scores for persisted upcoming fixtures."""
from __future__ import annotations

from dataclasses import replace
from datetime import date
from typing import Iterable

from spm.data.fixtures import Fixture
from spm.data.models import Match
from spm.data.normalization import canonical_team_name
from spm.statistics.engine import SPMEngine, SPMScore


def score_fixtures(
    matches: list[Match],
    fixtures: Iterable[Fixture],
    *,
    as_of: date,
    engine: SPMEngine | None = None,
) -> tuple[SPMScore, ...]:
    """Score upcoming fixtures, normalizing provider names to historical names."""
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
        home_team = canonical_team_name(fixture.home_team)
        away_team = canonical_team_name(fixture.away_team)
        try:
            score = scorer.score(matches, home_team, away_team, as_of)
            # Keep the provider's readable names in the public Live dashboard
            # while all statistical matching uses canonical historical names.
            scored.append(replace(score, home_team=fixture.home_team, away_team=fixture.away_team))
        except ValueError as exc:
            if "historical match" not in str(exc):
                raise
            skipped.append((fixture.home_team, fixture.away_team, str(exc)))

    if skipped:
        print(f"live_scoring,skipped={skipped}", flush=True)
    print(f"live_scoring,scores={len(scored)}", flush=True)
    return tuple(scored)
