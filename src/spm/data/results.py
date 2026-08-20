"""Canonical match-result model and CSV ingestion."""
from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path


@dataclass(frozen=True, slots=True)
class MatchResult:
    match_date: date
    home_team: str
    away_team: str
    home_goals: int
    away_goals: int

    @property
    def outcome(self) -> str:
        if self.home_goals == self.away_goals:
            return "D"
        return "H" if self.home_goals > self.away_goals else "A"


def load_match_results_csv(path: str | Path) -> tuple[MatchResult, ...]:
    """Load Date,HomeTeam,AwayTeam,HomeGoals,AwayGoals CSV records."""
    records: list[MatchResult] = []
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"Date", "HomeTeam", "AwayTeam", "HomeGoals", "AwayGoals"}
        missing = required.difference(reader.fieldnames or ())
        if missing:
            raise ValueError(f"missing CSV columns: {sorted(missing)}")
        for row in reader:
            records.append(
                MatchResult(
                    match_date=_parse_date(row["Date"]),
                    home_team=row["HomeTeam"].strip(),
                    away_team=row["AwayTeam"].strip(),
                    home_goals=int(row["HomeGoals"]),
                    away_goals=int(row["AwayGoals"]),
                )
            )
    return tuple(records)


def _parse_date(value: str) -> date:
    for fmt in ("%d/%m/%Y", "%d/%m/%y", "%Y-%m-%d"):
        try:
            return datetime.strptime(value.strip(), fmt).date()
        except ValueError:
            continue
    raise ValueError(f"unsupported date: {value}")
