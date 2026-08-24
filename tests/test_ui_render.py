from datetime import date

from spm.ui.contracts import DashboardSnapshot, FixtureCard
from spm.ui.render import render_dashboard


def test_render_dashboard_contains_snapshot_data() -> None:
    snapshot = DashboardSnapshot(
        as_of=date(2026, 8, 22),
        bankroll=1000.0,
        profit=25.5,
        drawdown=40.0,
        selections=(FixtureCard("Inter", "Milan", 87.0, 0.318, 3.45),),
    )
    html = render_dashboard(snapshot)
    assert "SPM_v2" in html
    assert "Inter" in html
    assert "Milan" in html
    assert "87" in html
    assert "31.8%" in html
    assert "3.45" in html
