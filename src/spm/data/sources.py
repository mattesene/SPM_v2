"""External football-data source registry and provenance model.

The registry deliberately separates *what a source provides* from *how data
is fetched*. Fetchers are implemented only where access is permitted and
stable; the model itself never depends on a particular website.
"""

from dataclasses import dataclass
from enum import StrEnum


class DataRole(StrEnum):
    RESULTS = "results"
    FIXTURES = "fixtures"
    TEAM_STATS = "team_stats"
    MATCH_STATS = "match_stats"
    PLAYER_STATS = "player_stats"
    CONTEXT = "context"
    ODDS = "odds"


@dataclass(frozen=True, slots=True)
class DataSource:
    name: str
    url: str
    roles: tuple[DataRole, ...]
    priority: int
    notes: str = ""


SOURCE_REGISTRY: tuple[DataSource, ...] = (
    DataSource(
        "Diretta.it",
        "https://www.diretta.it/",
        (DataRole.RESULTS, DataRole.FIXTURES, DataRole.ODDS),
        1,
        "Primary live/results and fixture reference; respect robots and site terms.",
    ),
    DataSource(
        "Sofascore",
        "https://www.sofascore.com/it",
        (DataRole.RESULTS, DataRole.FIXTURES, DataRole.TEAM_STATS, DataRole.MATCH_STATS, DataRole.PLAYER_STATS),
        1,
        "Primary rich statistical source when an authorized/stable access path is available.",
    ),
    DataSource(
        "FBref",
        "https://fbref.com/en/",
        (DataRole.RESULTS, DataRole.FIXTURES, DataRole.TEAM_STATS, DataRole.MATCH_STATS, DataRole.PLAYER_STATS),
        2,
        "Independent historical/statistical cross-check; broad competition coverage.",
    ),
    DataSource(
        "WhoScored",
        "https://it.whoscored.com/statistics",
        (DataRole.TEAM_STATS, DataRole.MATCH_STATS, DataRole.PLAYER_STATS),
        2,
        "Advanced statistics source; direct automated access may require a permitted access method.",
    ),
    DataSource(
        "CIES Football Observatory",
        "https://football-observatory.com/?lang=en",
        (DataRole.CONTEXT, DataRole.PLAYER_STATS, DataRole.TEAM_STATS),
        3,
        "Research/context source rather than the primary match-results feed.",
    ),
)


def sources_for(role: DataRole) -> tuple[DataSource, ...]:
    return tuple(source for source in SOURCE_REGISTRY if role in source.roles)
