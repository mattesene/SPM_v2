"""Deterministic real-dataset coverage check for the historical window."""
from __future__ import annotations

from spm.ingestion.historical import COMPETITIONS
from spm.ingestion.historical_batch import load_historical_batch
from spm.ingestion.historical_manifest import validate_coverage
from spm.ingestion.seasons import season_codes


def run_historical_coverage_check():
    records = load_historical_batch(COMPETITIONS, season_codes())
    return validate_coverage(records)
