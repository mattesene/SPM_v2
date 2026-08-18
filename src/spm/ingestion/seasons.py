"""Canonical historical season ranges used by SPM_v2."""
from __future__ import annotations

from collections.abc import Iterator


def season_codes(start: int = 2019, end: int = 2025) -> tuple[str, ...]:
    """Return Football-Data season codes from start year through end year."""
    if end < start:
        raise ValueError("end must be greater than or equal to start")
    return tuple(f"{year % 100:02d}{(year + 1) % 100:02d}" for year in range(start, end + 1))
