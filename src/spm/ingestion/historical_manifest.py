"""Manifest and coverage validation for the historical Football-Data dataset."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from spm.data.normalized import MatchRecord
from spm.ingestion.historical import COMPETITIONS
from spm.ingestion.seasons import HISTORICAL_SEASONS


@dataclass(frozen=True, slots=True)
class HistoricalCoverage:
    expected_slices: int
    present_slices: int
    missing_slices: tuple[tuple[str, str], ...]
    records: int
    competitions: int
    seasons: int


def validate_coverage(records: Iterable[MatchRecord]) -> HistoricalCoverage:
    rows = tuple(records)
    present = {(r.competition, r.season) for r in rows}
    expected = {(c, s) for c in COMPETITIONS for s in HISTORICAL_SEASONS}
    return HistoricalCoverage(
        expected_slices=len(expected),
        present_slices=len(present & expected),
        missing_slices=tuple(sorted(expected - present)),
        records=len(rows),
        competitions=len({r.competition for r in rows}),
        seasons=len({r.season for r in rows}),
    )
