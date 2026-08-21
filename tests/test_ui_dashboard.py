from datetime import date

from spm.statistics.engine import SPMScore
from spm.ui.dashboard import snapshot_from_ranked


def test_dashboard_snapshot_maps_canonical_ranking() -> None:
    ranked = [
        SPMScore(
            home_team="Inter",
            away_team="Milan",
            draw_probability=0.318,
            spm_score=87.0,
            form_balance=0.8,
            draw_signal=0.7,
            goal_balance_signal=0.9,
            weights=(0.6, 0.15, 0.15, 0.1),
        )
    ]
    snapshot = snapshot_from_ranked(
        ranked, as_of=date(2026, 8, 22), bankroll=1000.0, profit=25.0, drawdown=40.0
    )
    assert snapshot.bankroll == 1000.0
    assert snapshot.profit == 25.0
    assert snapshot.selections[0].home_team == "Inter"
    assert snapshot.selections[0].draw_probability == 0.318
    assert snapshot.selections[0].spm_score == 87.0
