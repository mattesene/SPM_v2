"""Bootstrap the Live SQLite database from the reproducible historical catalog."""
from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from spm.data.default_historical_catalog import default_catalog
from spm.data.historical_ingest import ingest_catalog
from spm.data.repository import MatchRepository
from spm.live.config import build_fixture_provider
from spm.live.pipeline import acquire_and_normalize


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default="data/live/spm.db")
    parser.add_argument("--cache", default="data/cache/historical")
    args = parser.parse_args()

    db_path = Path(args.db)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    cache = Path(args.cache)
    cache.mkdir(parents=True, exist_ok=True)

    repository = MatchRepository(db_path)
    result = ingest_catalog(default_catalog(), cache)
    written = 0
    for records in result.datasets.values():
        for record in records:
            repository.upsert(record)
            written += 1

    provider = build_fixture_provider()
    acquisition = acquire_and_normalize(provider, repository, from_date=date.today())
    print(
        f"historical_records={written}, matches={repository.count()}, "
        f"fixtures_seen={acquisition.fetched}, fixtures_written={acquisition.written}, "
        f"fixtures_rejected={acquisition.rejected}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
