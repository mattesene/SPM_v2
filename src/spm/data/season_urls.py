"""URL construction for Football-Data.co.uk historical result CSVs."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SeasonSource:
    competition: str
    season: str
    url: str
    filename: str


def football_data_season(competition: str, season: str) -> SeasonSource:
    """Build a Football-Data.co.uk CSV source for a four-digit season code.

    Football-Data stores the season-specific file under ``<season>/<league>.csv``
    (for example ``2425/E0.csv``), while the local cache keeps the season in the
    filename so all 35 sources remain uniquely addressable.
    """
    competition = competition.strip().upper()
    season = season.strip()
    if not competition or not season or len(season) != 4 or not season.isdigit():
        raise ValueError("competition and a four-digit numeric season are required")
    filename = f"{competition}{season}.csv"
    url = f"https://www.football-data.co.uk/mmz4281/{season}/{competition}.csv"
    return SeasonSource(competition, season, url, filename)
