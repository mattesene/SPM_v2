"""Standalone HTML dashboard rendering for SPM predictions."""
from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Iterable

from spm.statistics.engine import SPMScore


def render_dashboard(results: Iterable[SPMScore], *, as_of: str) -> str:
    rows = tuple(results)
    body = "\n".join(
        f'<tr><td><span class="rank">{index}</span></td><td><strong>{escape(item.home_team)}</strong><br><span class="muted">vs</span><br><strong>{escape(item.away_team)}</strong></td>'
        f'<td><span class="prob">{item.draw_probability:.1%}</span></td><td><strong>{item.spm_score:.1f}</strong></td>'
        f'<td>{item.form_balance:.1%}</td><td>{item.draw_signal:.1%}</td><td>{item.goal_balance_signal:.1%}</td></tr>'
        for index, item in enumerate(rows, start=1)
    )
    if not body:
        body = '<tr><td colspan="7" class="empty">Nessuna opportunità disponibile</td></tr>'
    return f'''<!doctype html>
<html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>SPM_v2 — Dashboard</title><style>
:root {{ color-scheme: dark; font-family: Inter,system-ui,-apple-system,sans-serif; }}
* {{ box-sizing:border-box }} body {{ margin:0; background:#080d18; color:#edf2f7; }} main {{ max-width:1180px; margin:0 auto; padding:42px 22px 70px; }}
.hero {{ display:flex; justify-content:space-between; gap:24px; align-items:end; margin-bottom:30px; }} h1 {{ margin:0; font-size:34px; letter-spacing:-.03em; }}
.subtitle {{ color:#91a0b7; margin-top:8px; }} .badge {{ padding:10px 14px; border:1px solid #2b3951; border-radius:999px; color:#c4d0e0; white-space:nowrap; }}
.card {{ background:#101827; border:1px solid #243249; border-radius:20px; overflow:hidden; box-shadow:0 20px 55px rgba(0,0,0,.25); }}
.table-wrap {{ overflow-x:auto }} table {{ width:100%; border-collapse:collapse; min-width:760px; }} th,td {{ padding:16px 14px; text-align:left; border-bottom:1px solid #202d42; }}
th {{ color:#8190a7; font-size:11px; text-transform:uppercase; letter-spacing:.08em; }} tbody tr:hover {{ background:#162033; }} tbody tr:first-child {{ background:#142238; }}
.rank {{ display:inline-flex; width:32px; height:32px; align-items:center; justify-content:center; border-radius:50%; background:#1b2b43; font-weight:700; }}
.prob {{ font-size:18px; font-weight:800; }} .muted {{ color:#718198; font-size:12px; }} .empty {{ text-align:center; color:#91a0b7; padding:48px; }}
@media(max-width:760px) {{ main {{ padding:26px 12px 50px; }} .hero {{ align-items:start; flex-direction:column; }} }}
</style></head><body><main><section class="hero"><div><h1>SPM_v2</h1><div class="subtitle">Top 5 opportunità di pareggio · analisi statistica</div></div>
<div class="badge">Analisi al {escape(as_of)}</div></section><section class="card"><div class="table-wrap"><table><thead><tr><th>#</th><th>Partita</th><th>Probabilità X</th><th>SPM Score</th><th>Forma</th><th>Segnale X</th><th>Equilibrio gol</th></tr></thead>
<tbody>{body}</tbody></table></div></section></main></body></html>'''


def write_dashboard(results: Iterable[SPMScore], *, as_of: str, path: str | Path) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(render_dashboard(results, as_of=as_of), encoding="utf-8")
