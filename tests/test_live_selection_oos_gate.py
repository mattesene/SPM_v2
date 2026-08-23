from datetime import date

from spm.backtest.oos_ranking import OOSRankingEntry
from spm.data.fixtures import Fixture
from spm.live.selection import select_live_candidates


def test_live_selection_requires_sufficient_oos_evidence():
    fixtures = [Fixture(date(2026, 8, 24), "A", "B")]
    weak = OOSRankingEntry("A vs B", 1, 2, 100.0, 0.10, 0.0, 1.0, 1.0)
    assert select_live_candidates(fixtures, [weak], min_bets=5) == ()


def test_live_selection_accepts_candidate_with_required_oos_sample():
    fixtures = [Fixture(date(2026, 8, 24), "A", "B")]
    strong = OOSRankingEntry("A vs B", 3, 10, 100.0, 0.10, 10.0, 0.66, 0.74)
    result = select_live_candidates(fixtures, [strong], min_bets=5)
    assert len(result) == 1
    assert result[0].key == "A vs B"
