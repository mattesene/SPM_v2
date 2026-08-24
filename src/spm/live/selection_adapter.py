"""Convert scored Live fixtures into persistent selection-history records."""
from __future__ import annotations

from datetime import date
from typing import Iterable

from spm.data.fixtures import Fixture
from spm.live.selection_history import LiveSelection
from spm.statistics.engine import SPMScore


def to_live_selections(
    scores: Iterable[SPMScore],
    fixtures: Iterable[Fixture],
    *,
    as_of: date,
    oos_scores: dict[str, float] | None = None,
    draw_odds: dict[tuple[date, str, str], float] | None = None,
    limit: int = 5,
) -> tuple[LiveSelection, ...]:
    """Create audit records without inventing bookmaker odds."""
    fixture_rows = tuple(fixtures)
    fixture_map = {(f.date, f.home_team.strip(), f.away_team.strip()): f for f in fixture_rows}
    ranked = sorted(scores, key=lambda item: item.spm_score, reverse=True)[:limit]
    result: list[LiveSelection] = []
    for rank, score in enumerate(ranked, 1):
        candidates = [f for (day, home, away), f in fixture_map.items()
                      if home == score.home_team.strip() and away == score.away_team.strip() and day >= as_of]
        if not candidates:
            continue
        fixture = min(candidates, key=lambda f: f.date)
        key = f"{score.home_team.strip()}|{score.away_team.strip()}"
        oos = oos_scores.get(key) if oos_scores else None
        combined = (score.spm_score + oos) / 2 if oos is not None else score.spm_score
        odds_key = (fixture.date, fixture.home_team.strip(), fixture.away_team.strip())
        odds = draw_odds.get(odds_key) if draw_odds else None
        result.append(LiveSelection(as_of, rank, fixture.home_team, fixture.away_team,
                                    fixture.date, score.draw_probability, odds,
                                    score.spm_score, oos, combined))
    return tuple(result)
