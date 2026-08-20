"""CSV importer for canonical historical football match data."""
from __future__ import annotations

import csv
from datetime import date
from io import TextIOBase
from typing import Iterable

from .normalization_adapter import canonicalize_matches
from .schema import HistoricalMatch
from .validation import validate_matches


_REQUIRED = {"date", "competition", "season", "home_team", "away_team", "home_goals", "away_goals"}


def import_matches_csv(source: TextIOBase | str) -> tuple[HistoricalMatch, ...]:
    """Import a CSV from a path or text stream and return validated canonical matches."""
    close = False
    if isinstance(source, str):
        source = open(source, "r", encoding="utf-8", newline="")
        close = True
    try:
        reader = csv.DictReader(source)
        fields = set(reader.fieldnames or ())
        missing = _REQUIRED - fields
        if missing:
            raise ValueError(f"missing required columns: {sorted(missing)}")
        matches: list[HistoricalMatch] = []
        for row in reader:
            odds = row.get("draw_odds")
            matches.append(HistoricalMatch(
                match_date=date.fromisoformat(row["date"]),
                competition=row["competition"].strip(),
                season=row["season"].strip(),
                home_team=row["home_team"].strip(),
                away_team=row["away_team"].strip(),
                home_goals=int(row["home_goals"]),
                away_goals=int(row["away_goals"]),
                draw_odds=float(odds) if odds not in (None, "") else None,
            ))
        return validate_matches(list(canonicalize_matches(matches)))
    finally:
        if close:
            source.close()
