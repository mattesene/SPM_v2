"""Determine whether persisted Live fixtures are still fresh."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone

from spm.data.repository import MatchRepository


@dataclass(frozen=True)
class LiveStatus:
    fresh: bool
    fixtures: int
    refreshed_at: datetime | None
    message: str


def inspect_live_status(repository: MatchRepository, *, today: date, max_age_hours: int = 12) -> LiveStatus:
    fixtures = repository.load_fixtures(from_date=today)
    refreshed_at = repository.fixtures_refreshed_at
    if refreshed_at is None:
        return LiveStatus(False, len(fixtures), None, "DATI LIVE NON AGGIORNATI")
    now = datetime.now(timezone.utc)
    if refreshed_at.tzinfo is None:
        refreshed_at = refreshed_at.replace(tzinfo=timezone.utc)
    fresh = now - refreshed_at <= timedelta(hours=max_age_hours)
    return LiveStatus(fresh, len(fixtures), refreshed_at, "LIVE AGGIORNATO" if fresh else "DATI LIVE DA AGGIORNARE")
