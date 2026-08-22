"""Deterministic football team-name normalization."""
from __future__ import annotations

import re
import unicodedata


def normalize_team_name(name: str) -> str:
    """Return a stable comparison key while preserving the original display name elsewhere."""
    if not isinstance(name, str):
        raise TypeError("team name must be a string")
    value = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    value = value.casefold().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return " ".join(value.split())


def same_team(left: str, right: str) -> bool:
    return normalize_team_name(left) == normalize_team_name(right)
