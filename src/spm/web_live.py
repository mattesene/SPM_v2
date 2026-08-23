"""Dashboard rendering for live SPM/OOS candidates."""
from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Iterable

from spm.backtest.live_selection import LiveCandidate


def render_live_dashboard(candidates: Iterable[LiveCandidate], *, as_of: str) -> str:
    rows = tuple(candidates)[:5]
    cards = []
    for index, item in enumerate(rows, 1):
        home, away = item.fixture
        cards.append(f'''<article class="card {'featured' if index == 1 else ''}">
<header><span class="rank">#{index}</span><span class="label">LIVE PICK</span></header>
<section class="fixture"><strong>{escape(home)}</strong><span> X </span><strong>{escape(away)}</strong></section>
<div class="scores"><div><small>Combined</small><b>{item.combined_score:.1f}</b></div><div><small>Confidence</small><b>{item.confidence:.1%}</b></div><div><small>SPM</small><b>{item.spm_score:.1f}</b></div><div><small>OOS</small><b>{item.oos_score:.1f}</b></div></div>
<div class="evidence"><span>OOS: {item.bets} bet</span><span>{item.profitable_window_rate:.0%} finestre profittevoli</span></div>
</article>''')
    body = ''.join(cards) or '<div class="empty">Nessuna selezione live disponibile</div>'
    return f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>SPM_v2 — Live</title>
<style>:root{{color-scheme:dark;font-family:Inter,system-ui,sans-serif}}*{{box-sizing:border-box}}body{{margin:0;background:#080d18;color:#edf2f7}}main{{max-width:1050px;margin:auto;padding:40px 20px 60px}}h1{{margin:0;font-size:34px}}.sub{{color:#91a0b7;margin:8px 0 28px}}.grid{{display:grid;gap:14px}}.card{{background:#101827;border:1px solid #243249;border-radius:20px;padding:20px}}.featured{{border-color:#466487}}header{{display:flex;justify-content:space-between;margin-bottom:20px}}.rank{{font-weight:800}}.label{{font-size:10px;letter-spacing:.1em;color:#91a0b7;border:1px solid #30415b;padding:6px 9px;border-radius:99px}}.fixture{{display:flex;justify-content:center;align-items:center;gap:14px;font-size:21px;margin-bottom:22px}}.fixture span{{color:#71819a}}.scores{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;border-top:1px solid #202d42;padding-top:16px}}.scores div{{display:flex;flex-direction:column;gap:5px}}small{{color:#71819a;text-transform:uppercase;font-size:10px}}b{{font-size:17px}}.evidence{{display:flex;gap:12px;margin-top:16px;color:#91a0b7;font-size:12px}}.empty{{padding:45px;text-align:center;color:#91a0b7;border:1px solid #243249;border-radius:20px}}@media(max-width:650px){{main{{padding:25px 12px}}.fixture{{font-size:17px}}.scores{{grid-template-columns:repeat(2,1fr)}}.evidence{{flex-direction:column}}}}</style></head><body><main><h1>SPM_v2 · Live</h1><div class="sub">Top 5 selezioni basate su SPM + evidenza OOS · analisi al {escape(as_of)}</div><section class="grid">{body}</section></main></body></html>'''


def write_live_dashboard(candidates: Iterable[LiveCandidate], *, as_of: str, path: str | Path) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(render_live_dashboard(candidates, as_of=as_of), encoding="utf-8")
