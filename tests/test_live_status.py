from datetime import date, datetime, timedelta, timezone

from spm.data.repository import MatchRepository
from spm.live.status import inspect_live_status


def test_live_status_is_fresh_after_recent_refresh(tmp_path):
    repo = MatchRepository(tmp_path / "spm.db")
    repo.mark_fixtures_refreshed(datetime.now(timezone.utc) - timedelta(hours=1))
    status = inspect_live_status(repo, today=date(2026, 8, 23), max_age_hours=12)
    assert status.fresh is True
    assert status.message == "LIVE AGGIORNATO"


def test_live_status_is_stale_after_threshold(tmp_path):
    repo = MatchRepository(tmp_path / "spm.db")
    repo.mark_fixtures_refreshed(datetime.now(timezone.utc) - timedelta(hours=13))
    status = inspect_live_status(repo, today=date(2026, 8, 23), max_age_hours=12)
    assert status.fresh is False
    assert status.message == "DATI LIVE DA AGGIORNARE"


def test_live_status_without_refresh_is_not_fresh(tmp_path):
    repo = MatchRepository(tmp_path / "spm.db")
    status = inspect_live_status(repo, today=date(2026, 8, 23))
    assert status.fresh is False
    assert status.message == "DATI LIVE NON AGGIORNATI"
