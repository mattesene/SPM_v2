from datetime import date

from spm.backtest.oos_pipeline import run_oos_from_temporal_split
from spm.data.models import Match
from spm.data.odds import DrawOdds


def test_temporal_pipeline_uses_only_oos_matches_and_odds():
    matches = [
        Match(date(2026, 8, 1), "A", "B", 1, 1),
        Match(date(2026, 8, 2), "A", "B", 0, 1),
        Match(date(2026, 8, 3), "A", "B", 1, 1),
        Match(date(2026, 8, 4), "A", "B", 2, 2),
        Match(date(2026, 8, 5), "A", "B", 1, 0),
    ]
    odds = [DrawOdds(m.date, "A", "B", 3.0) for m in matches]
    result = run_oos_from_temporal_split(
        matches,
        odds,
        cutoff=date(2026, 8, 3),
        initial_bankroll=1000.0,
        base_stake=10.0,
        min_bets=1,
        limit=5,
    )
    assert result
    assert result[0].bets == 3
