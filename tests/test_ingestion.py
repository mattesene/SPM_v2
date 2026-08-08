from datetime import date, datetime

from spm.data.normalized import MatchRecord
from spm.data.provenance import Provenance
from spm.data.repository import MatchRepository
from spm.ingestion.pipeline import IngestionPipeline
from spm.ingestion.protocol import FetchBatch


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
