"""Deterministic normalization helpers for provider team names."""
from dataclasses import dataclass
import re
import unicodedata


def normalize_team_name(name: str) -> str:
    value = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-zA-Z0-9]+", " ", value).strip().lower()
    return re.sub(r"\s+", " ", value)


@dataclass(frozen=True, slots=True)
class TeamAlias:
    canonical: str
    aliases: tuple[str, ...]


TEAM_ALIASES = (
    TeamAlias("inter", ("inter", "inter milan", "internazionale", "internazionale milano")),
    TeamAlias("milan", ("milan", "ac milan", "milan ac")),
    TeamAlias("roma", ("roma", "as roma", "roma fc")),
    TeamAlias("lazio", ("lazio", "ss lazio")),
)


def canonical_team_name(name: str) -> str:
    normalized = normalize_team_name(name)
    for alias in TEAM_ALIASES:
        if normalized in {normalize_team_name(value) for value in alias.aliases}:
            return alias.canonical
    return normalized
