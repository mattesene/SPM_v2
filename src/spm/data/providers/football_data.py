"""Adapter for Football-Data.co.uk result CSVs.

The adapter deliberately accepts a local CSV path. Downloading is kept outside
this module so scheduled jobs can enforce their own network and provenance
policy before handing data to SPM.
"""
from pathlib import Path

from ..csv import CSVMatchImporter
from ..normalized import MatchRecord
from ..provenance import Provenance


class FootballDataCSVProvider:
    SOURCE = "football-data.co.uk"
    RESULTS_URL = "https://www.football-data.co.uk/englandm.php"

    def __init__(self, competition: str | None = None, season: str | None = None) -> None:
        self.competition = competition
        self.season = season

    def load(self, path: str | Path) -> list[MatchRecord]:
        matches = CSVMatchImporter().load(path)
        records: list[MatchRecord] = []
        for index, match in enumerate(matches, start=2):
            records.append(
                MatchRecord(
                    date=match.date,
                    home_team=match.home_team,
                    away_team=match.away_team,
                    home_goals=match.home_goals,
                    away_goals=match.away_goals,
                    competition=self.competition,
                    season=self.season,
                    provenance=(
                        Provenance(
                            source=self.SOURCE,
                            source_id=f"{Path(path).name}:{index}",
                            source_url=self.RESULTS_URL,
                        ),
                    ),
                )
            )
        return records
