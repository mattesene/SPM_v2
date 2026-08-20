"""Parser for Football-Data.co.uk historical CSV files, including draw odds."""
from __future__ import annotations

import csv
from datetime import date, datetime
from pathlib import Path

from .normalized import MatchRecord
from .odds import DrawOdds

_DATE_FORMATS = ("%d/%m/%Y", "%d/%m/%y", "%d/%m/%Y %H:%M")
_ODDS_COLUMNS = ("B365D", "BWD", "IWD", "PSD", "WHDD", "VCDD", "MaxD", "AvgD")


def _parse_date(value: str) -> date:
    value = value.strip()
    for fmt in _DATE_FORMATS:
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            pass
    raise ValueError(f"unsupported match date: {value!r}")


def _float(value: str | None) -> float | None:
    if value is None or not value.strip():
        return None
    try:
        return float(value.strip())
    except ValueError:
        return None


def _int(value: str | None) -> int | None:
    if value is None or not value.strip():
        return None
    return int(float(value.strip()))


def load_football_data_csv(path: str | Path, *, competition: str | None = None, season: str | None = None) -> tuple[MatchRecord, ...]:
    rows: list[MatchRecord] = []
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG"}
        fields = set(reader.fieldnames or ())
        if not required.issubset(fields):
            raise ValueError(f"missing Football-Data columns: {sorted(required - fields)}")
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


def load_football_data_odds(path: str | Path) -> tuple[DrawOdds, ...]:
    """Load one draw price per match, preferring AvgD then MaxD then bookmakers."""
    odds: list[DrawOdds] = []
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = set(reader.fieldnames or ())
        available = [name for name in _ODDS_COLUMNS if name in fields]
        if not available:
            return ()
        for row in reader:
            draw_odds = None
            for column in ("AvgD", "MaxD", *available):
                draw_odds = _float(row.get(column))
                if draw_odds is not None and draw_odds > 1.0:
                    break
            if draw_odds is None or draw_odds <= 1.0:
                continue
            odds.append(DrawOdds(
                date=_parse_date(row["Date"]),
                home_team=row["HomeTeam"],
                away_team=row["AwayTeam"],
                draw_odds=draw_odds,
            ))
    return tuple(odds)
