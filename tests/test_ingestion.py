from datetime import date, datetime

from spm.data.normalized import MatchRecord
from spm.data.provenance import Provenance
from spm.data.repository import MatchRepository
from spm.ingestion.pipeline import IngestionPipeline
from spm.ingestion.protocol import FetchBatch
from spm.data.ingestion import IngestionService


def test_pipeline_reconciles_and_persists_sources(tmp_path) -> None:
    retrieved = datetime(2026, 8, 8, 12, 0)
    batches = [
        FetchBatch("sofascore", retrieved, (
            MatchRecord(date(2026, 8, 8), "Inter Milan", "AC Milan", 2, 1, "Serie A", "2026/27", (Provenance("sofascore", "s1"),)),
        )),
        FetchBatch("fbref", retrieved, (
            MatchRecord(date(2026, 8, 8), "Internazionale", "Milan", 2, 1, "Serie A", "2026/27", (Provenance("fbref", "f1"),)),
        )),
    ]
    repo = MatchRepository(tmp_path / "spm.db")
    assert IngestionPipeline(repo).ingest(batches) == 1
    assert repo.count() == 1
    assert repo.provenance_count() == 2


def test_incremental_ingestion_is_idempotent(tmp_path) -> None:
    repo = MatchRepository(tmp_path / "spm.db")
    service = IngestionService(repo)
    record = MatchRecord(date(2026, 8, 9), "A", "B", 1, 1, competition="Serie A")
    first = service.ingest([record])
    second = service.ingest([record])
    assert first.received == 1
    assert second.received == 1
    assert repo.count() == 1
    assert second.completed == 1


def test_filter_completed_respects_cutoff() -> None:
    records = [
        MatchRecord(date(2026, 8, 1), "A", "B", 1, 0),
        MatchRecord(date(2026, 8, 2), "A", "C"),
        MatchRecord(date(2026, 8, 3), "B", "C", 0, 0),
    ]
    result = IngestionService.filter_completed(records, date(2026, 8, 2))
    assert len(result) == 1
    assert result[0].home_team == "A"
