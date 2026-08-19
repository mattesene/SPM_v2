"""CSV importer for historical draw-market odds."""
from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

from .odds import DrawOdds


class DrawOddsCSVImporter:
    def __init__(
        self,
        *,
        date_column: str = "Date",
        home_column: str = "HomeTeam",
        away_column: str = "AwayTeam",
        draw_odds_column: str = "DrawOdds",
    ) -> None:
        self.date_column = date_column
        self.home_column = home_column
        self.away_column = away_column
        self.draw_odds_column = draw_odds_column

    def load(self, path: str | Path) -> list[DrawOdds]:
        with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            required = {
                self.date_column,
                self.home_column,
                self.away_column,
                self.draw_odds_column,
            }
            missing = required.difference(reader.fieldnames or ())
            if missing:
                raise ValueError(f"missing CSV columns: {sorted(missing)}")
            records: list[DrawOdds] = []
            for row in reader:
                if not row.get(self.date_column):
                    continue
                records.append(
                    DrawOdds(
                        date=_parse_date(row[self.date_column]),
                        home_team=row[self.home_column],
                        away_team=row[self.away_column],
                        draw_odds=float(row[self.draw_odds_column]),
                    )
                )
        return records


def _parse_date(value: str):
    for fmt in ("%d/%m/%Y", "%d/%m/%y", "%Y-%m-%d"):
        try:
            return datetime.strptime(value.strip(), fmt).date()
        except ValueError:
            pass
    raise ValueError(f"unsupported date: {value}")
