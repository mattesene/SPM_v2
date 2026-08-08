"""Adapter that promotes the existing CSV importer into canonical records."""
from datetime import datetime

from spm.data.csv import CSVMatchImporter
from spm.data.normalized import MatchRecord
from spm.data.provenance import Provenance

from .protocol import FetchBatch


class CSVSourceAdapter:
    source_name = "csv"

    def fetch(self, *, path: str, competition: str | None = None, season: str | None = None) -> FetchBatch:
        retrieved_at = datetime.now().astimezone()
        matches = CSVMatchImporter().load(path)
        records = tuple(
            MatchRecord(
                match.date,
                match.home_team,
                match.away_team,
                match.home_goals,
                match.away_goals,
                competition,
                season,
                (Provenance(self.source_name, source_url=str(path), retrieved_at=retrieved_at),),
            )
            for match in matches
        )
        return FetchBatch(self.source_name, retrieved_at, records)
