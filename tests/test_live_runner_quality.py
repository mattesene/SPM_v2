from datetime import date, timedelta

import pytest

from spm.data.fixtures import Fixture
from spm.data.models import Match
from spm.data.repository import MatchRepository
from spm.live.runner import run_live_from_database


def test_runner_blocks_stale_database(tmp_path):
    db = tmp_path / "live.db"
    repo = MatchRepository(db)
    as_of = date(2026, 8, 24)
    repo.upsert_fixture(Fixture("A", "B", as_of))
    # Keep the only completed result outside the accepted freshness window.
    from spm.data.normalized import MatchRecord
    repo.upsert(MatchRecord(as_of - timedelta(days=30), "C", "D", 1, 0))

    with pytest.raises(RuntimeError, match="data quality gate failed"):
        run_live_from_database(db, [], as_of=as_of, output=tmp_path / "index.html")


def test_runner_does_not_create_output_when_quality_fails(tmp_path):
    db = tmp_path / "live.db"
    repo = MatchRepository(db)
    as_of = date(2026, 8, 24)
    repo.upsert(Fixture("A", "A", as_of))
    from spm.data.normalized import MatchRecord
    repo.upsert(MatchRecord(as_of - timedelta(days=30), "C", "D", 1, 0))
    output = tmp_path / "index.html"

    with pytest.raises(RuntimeError):
        run_live_from_database(db, [], as_of=as_of, output=output)
    assert not output.exists()
