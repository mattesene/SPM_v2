"""Incremental ingestion orchestration for normalized match providers."""
from dataclasses import dataclass
from datetime import date

from .normalized import MatchRecord
from .repository import MatchRepository


@dataclass(frozen=True, slots=True)
class IngestionReport:
    received: int
    stored: int
    completed: int


class IngestionService:
    def __init__(self, repository: MatchRepository) -> None:
        self.repository = repository

    def ingest(self, records: list[MatchRecord]) -> IngestionReport:
        stored = 0
        completed = 0
        for record in records:
            self.repository.upsert(record)
            stored += 1
            if record.completed:
                completed += 1
        return IngestionReport(len(records), stored, completed)

    @staticmethod
    def filter_completed(records: list[MatchRecord], until: date | None = None) -> list[MatchRecord]:
        return [
            record for record in records
            if record.completed and (until is None or record.date <= until)
        ]
