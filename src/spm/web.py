"""Standalone HTML dashboard rendering for SPM predictions."""
from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Iterable

from spm.statistics.engine import SPMScore


def render_dashboard(results: Iterable[SPMScore], *, as_of: str, live: bool = False, source_status: str = "DATI STORICI") -> str:
    rows = tuple(results)[:5]
    cards = "\n".join(
        f'''<article class="opportunity {'featured' if index == 1 else ''}">
<div class="op-head"><span class="rank">#{index}</span><span class="tag">OPPORTUNITÀ</span></div>
<div class="fixture"><div><strong>{escape(item.home_team)}</strong><span>Casa</span></div><div class="vs">X</div><div><strong>{escape(item.away_team)}</strong><span>Ospite</span></div></div>
<div class="metrics"><div><small>Probabilità X</small><b>{item.draw_probability:.1%}</b></div><div><small>SPM Score</small><b>{item.spm_score:.1f}</b></div><div><small>Forma</small><b>{item.form_balance:.1%}</b></div><div><small>Segnale X</small><b>{item.draw_signal:.1%}</b></div><div><small>Equilibrio gol</small><b>{item.goal_balance_signal:.1%}</b></div></div>
</article>'''
        for index, item in enumerate(rows, start=1)
    )
    if not cards:
        cards = '<div class="empty">Nessuna opportunità disponibile</div>'
    mode = "LIVE" if live else "ANALISI"
    return f'''<!doctype html>
<html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>SPM_v2 — Dashboard</title><style>
:root {{ color-scheme: dark; font-family: Inter,system-ui,-apple-system,sans-serif; }} * {{ box-sizing:border-box }} body {{ margin:0; background:#080d18; color:#edf2f7; }} main {{ max-width:1120px; margin:0 auto; padding:42px 22px 70px; }}
.hero {{ display:flex; justify-content:space-between; gap:24px; align-items:end; margin-bottom:32px; }} h1 {{ margin:0; font-size:36px; letter-spacing:-.04em; }} .subtitle {{ color:#91a0b7; margin-top:8px; }} .status {{ display:flex; gap:8px; align-items:center; }} .badge {{ padding:9px 13px; border:1px solid #2b3951; border-radius:999px; color:#c4d0e0; white-space:nowrap; font-size:12px; }} .live {{ border-color:#385f51; color:#9ad7bb; }} .dot {{ width:7px; height:7px; border-radius:50%; background:#75c59e; display:inline-block; }}
.grid {{ display:grid; gap:14px; }} .opportunity {{ background:#101827; border:1px solid #243249; border-radius:20px; padding:20px; box-shadow:0 14px 38px rgba(0,0,0,.18); }} .opportunity.featured {{ border-color:#3b5578; background:#121e30; }} .op-head {{ display:flex; align-items:center; justify-content:space-between; margin-bottom:20px; }} .rank {{ font-weight:800; font-size:16px; }} .tag {{ font-size:10px; letter-spacing:.1em; color:#8fa1bb; border:1px solid #30415b; padding:6px 9px; border-radius:999px; }}
.fixture {{ display:grid; grid-template-columns:1fr 46px 1fr; align-items:center; gap:12px; margin-bottom:20px; }} .fixture div:not(.vs) {{ display:flex; flex-direction:column; gap:4px; }} .fixture div:last-child {{ text-align:right; }} .fixture strong {{ font-size:20px; }} .fixture span {{ color:#74849d; font-size:11px; text-transform:uppercase; }} .vs {{ width:40px; height:40px; display:flex; align-items:center; justify-content:center; border-radius:50%; background:#1b2b43; color:#a9bad2; font-weight:800; }}
.metrics {{ display:grid; grid-template-columns:repeat(5,1fr); border-top:1px solid #202d42; padding-top:16px; gap:10px; }} .metrics div {{ display:flex; flex-direction:column; gap:5px; }} .metrics small {{ color:#74849d; font-size:10px; text-transform:uppercase; letter-spacing:.06em; }} .metrics b {{ font-size:16px; }} .empty {{ padding:48px; text-align:center; color:#91a0b7; background:#101827; border:1px solid #243249; border-radius:20px; }}
@media(max-width:760px) {{ main {{ padding:26px 12px 50px; }} .hero {{ align-items:start; flex-direction:column; }} .metrics {{ grid-template-columns:repeat(2,1fr); }} .fixture strong {{ font-size:17px; }} }}
</style></head><body><main><section class="hero"><div><h1>SPM_v2</h1><div class="subtitle">Top 5 opportunità di pareggio · {mode}</div></div><div class="status"><div class="badge {'live' if live else ''}">{'<span class="dot"></span> ' if live else ''}{escape(source_status)}</div><div class="badge">Analisi al {escape(as_of)}</div></div></section><section class="grid">{cards}</section></main></body></html>'''


def write_dashboard(results: Iterable[SPMScore], *, as_of: str, path: str | Path, live: bool = False, source_status: str = "DATI STORICI") -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(render_dashboard(results, as_of=as_of, live=live, source_status=source_status), encoding="utf-8")
