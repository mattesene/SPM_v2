"""External football-data source registry and provenance model."""

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
    DataSource("Diretta.it", "https://www.diretta.it/", (DataRole.RESULTS, DataRole.FIXTURES, DataRole.ODDS), 1, "Primary live/results and fixture reference; respect robots and site terms."),
    DataSource("Sofascore", "https://www.sofascore.com/it", (DataRole.RESULTS, DataRole.FIXTURES, DataRole.TEAM_STATS, DataRole.MATCH_STATS, DataRole.PLAYER_STATS), 1, "Rich statistical source when an authorized/stable access path is available."),
    DataSource("FBref", "https://fbref.com/en/", (DataRole.RESULTS, DataRole.FIXTURES, DataRole.TEAM_STATS, DataRole.MATCH_STATS, DataRole.PLAYER_STATS), 2, "Historical/statistical cross-check; automated use must comply with site terms."),
    DataSource("WhoScored", "https://it.whoscored.com/statistics", (DataRole.TEAM_STATS, DataRole.MATCH_STATS, DataRole.PLAYER_STATS), 2, "Advanced statistics source; use only a permitted access method."),
    DataSource("CIES Football Observatory", "https://football-observatory.com/?lang=en", (DataRole.CONTEXT, DataRole.PLAYER_STATS, DataRole.TEAM_STATS), 3, "Research/context source rather than the primary results feed."),
    DataSource("Football-Data.co.uk", "https://www.football-data.co.uk/", (DataRole.RESULTS, DataRole.FIXTURES, DataRole.MATCH_STATS, DataRole.ODDS), 1, "Free computer-ready historical CSV/Excel data; use as the bootstrap/backtest feed."),
)


def sources_for(role: DataRole) -> tuple[DataSource, ...]:
    return tuple(source for source in SOURCE_REGISTRY if role in source.roles)
