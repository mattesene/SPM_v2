"""Parser for Football-Data.co.uk historical CSV files."""
from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from typing import Iterable

from .normalized import MatchRecord


_DATE_FORMATS = ("%d/%m/%Y", "%d/%m/%y", "%d/%m/%Y %H:%M")


def _parse_date(value: str):
    value = value.strip()
    for fmt in _DATE_FORMATS:
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            pass
    raise ValueError(f"unsupported match date: {value!r}")


def _int(value: str | None) -> int | None:
    if value is None or not value.strip():
        return None
    return int(float(value.strip()))


def load_football_data_csv(path: str | Path, *, competition: str | None = None, season: str | None = None) -> tuple[MatchRecord, ...]:
    """Load completed and scheduled Football-Data rows without guessing columns."""
    rows: list[MatchRecord] = []
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG"}
        if not required.issubset(set(reader.fieldnames or ())):
            raise ValueError(f"missing Football-Data columns: {sorted(required - set(reader.fieldnames or ())) }")
        for row in reader:
            rows.append(MatchRecord(
                date=_parse_date(row["Date"]),
                home_team=row["HomeTeam"],
                away_team=row["AwayTeam"],
                home_goals=_int(row.get("FTHG")),
                away_goals=_int(row.get("FTAG")),
                competition=competition,
                season=season,
            ))
    return tuple(rows)
