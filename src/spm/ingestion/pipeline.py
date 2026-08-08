"""Ingestion orchestration: fetch, reconcile, persist."""
from .protocol import FetchBatch
from spm.data.reconcile import reconcile
from spm.data.repository import MatchRepository


class IngestionPipeline:
    def __init__(self, repository: MatchRepository) -> None:
        self.repository = repository

    def ingest(self, batches: list[FetchBatch]) -> int:
        records = [record for batch in batches for record in batch.records]
        canonical = reconcile(records)
        for record in canonical:
            self.repository.upsert(record)
        return len(canonical)
