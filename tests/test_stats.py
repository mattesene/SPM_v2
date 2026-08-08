from datetime import date

import pytest

from spm.data.normalized import MatchRecord
from spm.data.repository import MatchRepository
from spm.data.stats import MatchStats


def test_match_stats_validation_and_persistence(tmp_path) -> None:
    match = MatchRecord(date(2026, 8, 8), "Inter", "Milan", 2, 1, "Serie A", "2026/27")
    stats = MatchStats(match.identity_key, "sofascore", xg_home=1.8, xg_away=0.9, possession_home=55, possession_away=45)
    assert stats.has_xg
    repo = MatchRepository(tmp_path / "spm.db")
    repo.upsert(match)
    repo.upsert_stats(stats)
    assert repo.stats_count() == 1


def test_invalid_xg_is_rejected() -> None:
    with pytest.raises(ValueError):
        MatchStats((date(2026, 8, 8), "a", "b", "Serie A"), "sofascore", xg_home=-1)
