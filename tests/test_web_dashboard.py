from datetime import date

from spm.statistics.engine import SPMScore
from spm.web import render_dashboard


def score(home: str, away: str) -> SPMScore:
    return SPMScore(home, away, .32, 82.5, .74, .81, .69, (.55, .25, .20, .10))


def test_dashboard_renders_top_five_cards():
    html = render_dashboard([score(f"H{i}", f"A{i}") for i in range(7)], as_of="2026-08-23")
    assert html.count('class="opportunity ') == 5
    assert "SPM_v2" in html
    assert "H0" in html
    assert "H5" not in html


def test_dashboard_handles_empty_results():
    html = render_dashboard([], as_of="2026-08-23")
    assert "Nessuna opportunità disponibile" in html
