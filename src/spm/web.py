"""Standalone HTML dashboard rendering for SPM predictions."""
from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Iterable

from spm.statistics.engine import SPMScore


def render_dashboard(results: Iterable[SPMScore], *, as_of: str) -> str:
    rows = tuple(results)
    body = "\n".join(
        f'<tr><td>{index}</td><td>{escape(item.home_team)}</td><td>{escape(item.away_team)}</td>'
        f'<td>{item.draw_probability:.1%}</td><td><strong>{item.spm_score:.1f}</strong></td>'
        f'<td>{item.form_balance:.1%}</td><td>{item.draw_signal:.1%}</td><td>{item.goal_balance_signal:.1%}</td></tr>'
        for index, item in enumerate(rows, start=1)
    )
    if not body:
        body = '<tr><td colspan="8" class="empty">Nessuna partita da visualizzare</td></tr>'
    return f'''<!doctype html>
<html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>SPM_v2 — Dashboard</title><style>
:root {{ color-scheme: dark; font-family: Inter,system-ui,-apple-system,sans-serif; }}
body {{ margin:0; background:#0b1020; color:#edf2f7; }} main {{ max-width:1180px; margin:0 auto; padding:40px 22px 60px; }}
.hero {{ display:flex; justify-content:space-between; gap:24px; align-items:end; margin-bottom:28px; }} h1 {{ margin:0; font-size:32px; }}
.subtitle {{ color:#9aa7bd; margin-top:8px; }} .badge {{ padding:9px 13px; border:1px solid #2a3954; border-radius:999px; color:#b9c7dc; }}
.card {{ background:#121a2b; border:1px solid #25334d; border-radius:18px; overflow:hidden; box-shadow:0 18px 45px rgba(0,0,0,.2); }}
table {{ width:100%; border-collapse:collapse; }} th,td {{ padding:15px 14px; text-align:left; border-bottom:1px solid #22304a; }}
th {{ color:#9aa7bd; font-size:12px; text-transform:uppercase; letter-spacing:.06em; }} tbody tr:hover {{ background:#182239; }} tbody tr:first-child td {{ background:#17243a; }}
.empty {{ text-align:center; color:#9aa7bd; padding:40px; }} @media(max-width:760px) {{ main {{ padding:24px 12px; }} .hero {{ align-items:start; flex-direction:column; }} .card {{ overflow-x:auto; }} table {{ min-width:760px; }} }}
</style></head><body><main><section class="hero"><div><h1>SPM_v2</h1><div class="subtitle">Statistical Pareggio Model · Top 5 opportunità filtrate</div></div>
<div class="badge">Analisi al {escape(as_of)}</div></section><section class="card"><table><thead><tr><th>#</th><th>Casa</th><th>Ospite</th><th>Pareggio</th><th>SPM Score</th><th>Forma</th><th>Segnale X</th><th>Equilibrio gol</th></tr></thead>
<tbody>{body}</tbody></table></section></main></body></html>'''


def write_dashboard(results: Iterable[SPMScore], *, as_of: str, path: str | Path) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(render_dashboard(results, as_of=as_of), encoding="utf-8")
