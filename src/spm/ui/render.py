"""Framework-neutral HTML renderer for the first SPM_v2 dashboard preview."""
from __future__ import annotations

from html import escape

from spm.ui.contracts import DashboardSnapshot


def render_dashboard(snapshot: DashboardSnapshot) -> str:
    rows = "".join(
        f"<tr><td>{escape(card.home_team)}</td><td>{escape(card.away_team)}</td>"
        f"<td>{card.spm_score:.0f}</td><td>{card.draw_probability:.1%}</td>"
        f"<td>{card.draw_odds if card.draw_odds is not None else '—'}</td></tr>"
        for card in snapshot.selections
    )
    return f"""<!doctype html>
<html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>SPM_v2 Dashboard</title>
<style>
body{{font-family:system-ui,sans-serif;margin:0;background:#f5f6f8;color:#18202a}}
main{{max-width:1100px;margin:auto;padding:24px}}
header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}}
.card{{background:white;border:1px solid #e1e5ea;border-radius:12px;padding:18px}}
.value{{font-size:28px;font-weight:700;margin-top:6px}}
table{{width:100%;border-collapse:collapse;background:white;border-radius:12px;overflow:hidden}}
th,td{{padding:13px;text-align:left;border-bottom:1px solid #edf0f2}}
@media(max-width:700px){{.grid{{grid-template-columns:1fr}};main{{padding:14px}}}}
</style></head><body><main>
<header><h1>SPM_v2</h1><span>Dashboard · {snapshot.as_of.isoformat()}</span></header>
<section class="grid">
<div class="card">BANKROLL<div class="value">€ {snapshot.bankroll:,.2f}</div></div>
<div class="card">PROFITTO<div class="value">€ {snapshot.profit:,.2f}</div></div>
<div class="card">DRAWDOWN<div class="value">€ {snapshot.drawdown:,.2f}</div></div>
</section>
<h2>Selezioni</h2><table><thead><tr><th>Casa</th><th>Trasferta</th><th>SPM</th><th>Pareggio</th><th>Quota</th></tr></thead><tbody>{rows}</tbody></table>
</main></body></html>"""
