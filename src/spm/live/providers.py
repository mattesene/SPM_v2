"""Concrete provider adapters for Live fixture acquisition."""
from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

from spm.live.normalization import RawFixture


class CSVFixtureProvider:
    """Read normalized external fixture exports without network dependencies."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def fetch_fixtures(self, from_date: date) -> list[RawFixture]:
        if not self.path.is_file():
            raise FileNotFoundError(f"fixture source not found: {self.path}")
        result: list[RawFixture] = []
        with self.path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                kickoff = date.fromisoformat(row["kickoff"])
                if kickoff >= from_date:
                    result.append(RawFixture(row["home"], row["away"], kickoff))
        return result
