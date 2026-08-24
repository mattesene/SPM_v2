from datetime import date

from spm.live.web_live import render_live_dashboard


def test_live_dashboard_empty_state():
    html = render_live_dashboard([], as_of="2026-08-24")
    assert "Nessuna selezione live disponibile" in html
    assert "Top 5 selezioni" in html


def test_live_dashboard_contains_status_and_date():
    html = render_live_dashboard([], as_of=date(2026, 8, 24).isoformat(), live_status="SPM ONLY")
    assert "SPM ONLY" in html
    assert "2026-08-24" in html
