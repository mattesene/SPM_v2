"""Adapter for the openly published Football-Data CSV files.

This adapter is intentionally limited to the site's published CSV endpoints;
it does not scrape HTML pages or bypass access controls.
"""

from csv import DictReader
from datetime import date, datetime, timezone
from io import TextIOWrapper
from urllib.request import Request, urlopen

from spm.data.normalized import MatchRecord
from spm.data.provenance import Provenance
from spm.ingestion.protocol import FetchBatch


class FootballDataAdapter:
    source_name = "Football-Data.co.uk"
    BASE_URL = "https://www.football-data.co.uk/mmz4281"

    def fetch(self, season: str = "2526", competition: str = "I1") -> FetchBatch:
        """Fetch a published CSV season, e.g. Serie A 2025/26 (2526/I1)."""
        url = f"{self.BASE_URL}/{season}/{competition}.csv"
        request = Request(url, headers={"User-Agent": "SPM_v2/0.3 (data importer)"})
        retrieved = datetime.now(timezone.utc)
        with urlopen(request, timeout=20) as response:
            rows = DictReader(TextIOWrapper(response, encoding="latin-1", newline=""))
            records = tuple(self._record(row, url, retrieved, season, competition) for row in rows if row.get("Date"))
        return FetchBatch(self.source_name, retrieved, records)

    @staticmethod
    def _record(row: dict[str, str], url: str, retrieved: datetime, season: str, competition: str) -> MatchRecord:
        day, month, year = row["Date"].split("/")
        year = f"20{year}" if len(year) == 2 else year
        return MatchRecord(
            date=date(int(year), int(month), int(day)),
            home_team=row["HomeTeam"].strip(),
            away_team=row["AwayTeam"].strip(),
            home_goals=_integer(row.get("FTHG")),
            away_goals=_integer(row.get("FTAG")),
            competition=competition,
            season=season,
            provenance=(Provenance("football-data", source_id=f"{season}/{competition}/{row['Date']}/{row['HomeTeam']}/{row['AwayTeam']}", source_url=url, retrieved_at=retrieved),),
        )


def _integer(value: str | None) -> int | None:
    if value is None or value == "":
        return None
    return int(float(value))
