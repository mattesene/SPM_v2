from datetime import date

from spm.backtest.live_selection import LiveCandidate
from spm.web_live import render_live_dashboard


def candidate(home="Inter", away="Milan", confidence=.72):
    return LiveCandidate((home, away), confidence, 82.0, 78.0, 88.0, 60)


def test_live_dashboard_displays_fresh_status_and_summary():
    html = render_live_dashboard([candidate()], as_of=date(2026, 8, 23).isoformat(), live_status="LIVE AGGIORNATO")
    assert "LIVE AGGIORNATO" in html
    assert "OPPORTUNITÀ VALIDE" in html
    assert "Inter" in html
    assert "Milan" in html
    assert "72.0%" in html


def test_live_dashboard_displays_stale_status():
    html = render_live_dashboard([], as_of="2026-08-23", live_status="DATI LIVE DA AGGIORNARE")
    assert "DATI LIVE DA AGGIORNARE" in html
    assert "Nessuna selezione live disponibile" in html
