from spm.statistics.engine import SPMScore
from spm.web import render_dashboard


def test_render_dashboard_contains_ranked_fixture_and_escaped_team() -> None:
    result = SPMScore(
        "Inter & Co", "Milan", 0.274, 27.4, 0.8, 0.7, 0.6, (0.6, 0.15, 0.15, 0.1)
    )
    html = render_dashboard([result], as_of="2026-08-22")
    assert "Inter &amp; Co" in html
    assert "Milan" in html
    assert "27.4" in html
    assert "27.4%" in html
    assert "2026-08-22" in html


def test_render_dashboard_handles_empty_results() -> None:
    html = render_dashboard([], as_of="2026-08-22")
    assert "Nessuna partita da visualizzare" in html
