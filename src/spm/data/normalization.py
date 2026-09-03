"""Deterministic normalization helpers for provider team names."""
from dataclasses import dataclass
import re
import unicodedata


def normalize_team_name(name: str) -> str:
    """Normalize a provider team name into a stable comparison key."""
    if not isinstance(name, str) or not name.strip():
        raise ValueError("team name must be a non-empty string")
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
    TeamAlias("sociedad", ("sociedad", "real sociedad")),
    TeamAlias("celta", ("celta", "celta vigo")),
    TeamAlias("stuttgart", ("stuttgart", "stoccarda", "vfb stuttgart")),
    TeamAlias("koeln", ("koeln", "koln", "kolonia", "colonia", "fc koln", "fc kolonia", "1 fc koln", "1 fc kolonia", "1 f c koln", "1 f c kolonia")),
    TeamAlias("betis", ("betis", "real betis")),
    TeamAlias("birmingham", ("birmingham", "birmingham city")),
    TeamAlias("wolverhampton", ("wolverhampton", "wolverhampton wanderers", "wolves")),
)

# Build the lookup once. The previous implementation normalized every alias on
# every team-name comparison, which made historical backtests unnecessarily
# expensive because normalization is called millions of times.
_ALIAS_TO_CANONICAL = {
    normalize_team_name(alias): group.canonical
    for group in TEAM_ALIASES
    for alias in group.aliases
}


def canonical_team_name(name: str) -> str:
    """Return the stable canonical key for a provider team name."""
    normalized = normalize_team_name(name)
    return _ALIAS_TO_CANONICAL.get(normalized, normalized)
