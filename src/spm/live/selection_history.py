"""Persistent audit trail for Live Top-5 selections."""
from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable

@dataclass(frozen=True, slots=True)
class LiveSelection:
    as_of: date
    rank: int
    home_team: str
    away_team: str
    fixture_date: date
    probability: float
    draw_odds: float | None
    spm_score: float
    oos_score: float | None
    combined_score: float

def append_selections(path: str | Path, selections: Iterable[LiveSelection]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    rows = tuple(selections)
    if not rows:
        return
    fields = tuple(LiveSelection.__dataclass_fields__)
    exists = target.exists() and target.stat().st_size > 0
    with target.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        if not exists:
            writer.writeheader()
        for row in rows:
            writer.writerow({name: getattr(row, name) for name in fields})

def load_selections(path: str | Path) -> tuple[LiveSelection, ...]:
    target = Path(path)
    if not target.is_file():
        return ()
    with target.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        result = []
        for row in reader:
            result.append(LiveSelection(
                as_of=date.fromisoformat(row["as_of"]), rank=int(row["rank"]),
                home_team=row["home_team"], away_team=row["away_team"],
                fixture_date=date.fromisoformat(row["fixture_date"]),
                probability=float(row["probability"]),
                draw_odds=float(row["draw_odds"]) if row["draw_odds"] else None,
                spm_score=float(row["spm_score"]),
                oos_score=float(row["oos_score"]) if row["oos_score"] else None,
                combined_score=float(row["combined_score"]),
            ))
        return tuple(result)
