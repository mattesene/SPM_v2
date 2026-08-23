from datetime import date

from spm.backtest.live_pipeline import build_live_top5
from spm.backtest.oos_ranking import OOSRankingEntry
from spm.data.fixtures import Fixture
from spm.data.repository import MatchRepository
from spm.live.normalization import RawFixture
from spm.live.pipeline import acquire_and_normalize
from spm.statistics.engine import SPMScore


class Provider:
    def fetch_fixtures(self, from_date):
        return [
            RawFixture("  Team   A", "Team B ", date(2026, 8, 24)),
            RawFixture("Team A", "Team B", date(2026, 8, 24)),
            RawFixture("", "Team C", date(2026, 8, 25)),
            Fixture("Team D", "Team D", date(2026, 8, 26)),
        ]


def test_live_pipeline_is_capped_at_five() -> None:
    scores = [SPMScore(f"H{i}", f"A{i}", .30, 30.0, .8, .8, .8, (.6, .15, .15, .1)) for i in range(7)]
    evidence = [OOSRankingEntry(f"H{i} vs A{i}", 2, 20, 100.0, .1, .0, .8, 1.0) for i in range(7)]
    result = build_live_top5(scores, evidence, min_bets=20)
    assert len(result) == 5


def test_acquire_and_normalize_applies_quality_gate(tmp_path):
    repo = MatchRepository(tmp_path / "spm.db")
    result = acquire_and_normalize(Provider(), repo, from_date=date(2026, 8, 23))
    assert result.fetched == 4
    assert result.written == 1
    assert result.rejected == 2
    assert result.duplicates_removed == 1
    fixtures = repo.load_fixtures(from_date=date(2026, 8, 23))
    assert fixtures == [Fixture("Team A", "Team B", date(2026, 8, 24))]
