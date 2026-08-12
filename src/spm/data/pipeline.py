"""End-to-end local ingestion pipeline for normalized football records."""
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from .ingestion import IngestionReport, IngestionService
from .normalized import MatchRecord
from .quality import validate_records
from .reconcile import reconcile
from .repository import MatchRepository
from .providers.football_data import FootballDataCSVProvider


@dataclass(frozen=True, slots=True)
class PipelineReport:
    received: int
    rejected: int
    stored: int
    completed: int


def ingest_football_data_csv(
    path: str | Path,
    repository: MatchRepository,
    *,
    competition: str | None = None,
    season: str | None = None,
    as_of: date | None = None,
) -> PipelineReport:
    records: list[MatchRecord] = FootballDataCSVProvider(competition, season).load(path)
    issues = validate_records(records, as_of=as_of)
    bad_indexes = {issue.record_index for issue in issues}
    clean = [record for index, record in enumerate(records) if index not in bad_indexes]
    clean = reconcile(clean)
    report: IngestionReport = IngestionService(repository).ingest(clean)
    return PipelineReport(len(records), len(bad_indexes), report.stored, report.completed)
