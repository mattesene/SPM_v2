"""Rolling chronological OOS windows."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Sequence


@dataclass(frozen=True, slots=True)
class OOSWindow:
    train_start: date
    train_end: date
    validation_end: date
    oos_start: date
    oos_end: date


def build_rolling_windows(dates: Sequence[date], *, train_years: int = 3, validation_years: int = 1, oos_years: int = 1) -> tuple[OOSWindow, ...]:
    if not dates:
        return ()
    if min(train_years, validation_years, oos_years) < 1:
        raise ValueError("window lengths must be positive")
    first, last = min(dates), max(dates)
    windows: list[OOSWindow] = []
    year = first.year + train_years + validation_years
    while year + oos_years - 1 <= last.year:
        train_start = date(year - train_years - validation_years, 1, 1)
        train_end = date(year - validation_years, 1, 1)
        validation_end = date(year, 1, 1)
        oos_start = validation_end
        oos_end = date(year + oos_years, 1, 1)
        windows.append(OOSWindow(train_start, train_end, validation_end, oos_start, oos_end))
        year += oos_years
    return tuple(windows)
