from datetime import date

from spm.backtest.oos_pipeline import run_oos_from_matches
from spm.data.models import Match
from spm.data.odds import DrawOdds


def test_oos_pipeline_can_start_from_domain_matches_and_odds():
    matches = [
        Match(date(2026, 8, i), "A", "B", 1, 1) for i in range(1, 6)
    ]
    odds = [
        DrawOdds(date(2026, 8, i), "A", "B", 3.0) for i in range(1, 6)
    ]
    result = run_oos_from_matches(
        matches,
        odds,
        initial_bankroll=1000.0,
        base_stake=10.0,
        min_bets=5,
        limit=5,
    )
    assert result
    assert result[0].bets == 5
