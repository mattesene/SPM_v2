"""CSV ingestion for standard football result datasets."""

import csv
from datetime import date, datetime
from pathlib import Path
from typing import Iterable

from .models import Match


class CSVMatchImporter:
    """Import matches from CSV files using explicit column names."""

    def __init__(self, date_column="Date", home_column="HomeTeam", away_column="AwayTeam", home_goals_column="FTHG", away_goals_column="FTAG"):
        self.date_column = date_column
        self.home_column = home_column
        self.away_column = away_column
        self.home_goals_column = home_goals_column
        self.away_goals_column = away_goals_column

    def load(self, path: str | Path) -> list[Match]:
        with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            required = {self.date_column, self.home_column, self.away_column, self.home_goals_column, self.away_goals_column}
            missing = required - set(reader.fieldnames or ())
            if missing:
                raise ValueError(f"Missing CSV columns: {', '.join(sorted(missing))}")
            return list(self._parse_rows(reader))

    def _parse_rows(self, rows: Iterable[dict[str, str]]) -> Iterable[Match]:
        for row_number, row in enumerate(rows, start=2):
            try:
                yield Match(
                    date=_parse_date(row[self.date_column]),
                    home_team=row[self.home_column].strip(),
                    away_team=row[self.away_column].strip(),
                    home_goals=int(row[self.home_goals_column]),
                    away_goals=int(row[self.away_goals_column]),
                )
            except (KeyError, TypeError, ValueError) as exc:
                raise ValueError(f"Invalid match data at CSV row {row_number}") from exc


def _parse_date(value: str) -> date:
    value = value.strip()
    for fmt in ("%d/%m/%Y", "%d/%m/%y", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            pass
    raise ValueError(f"Unsupported date format: {value}")
