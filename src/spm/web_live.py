"""Production live SPM/OOS dashboard renderer."""
from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Iterable

from spm.backtest.live_selection import LiveCandidate


def _confidence_class(value: float) -> str:
    if value >= 0.70:
        return "high"
    if value >= 0.55:
        return "medium"
    return "low"


def _oos_quality(item: LiveCandidate, *, has_oos: bool) -> tuple[str, str]:
    if not has_oos:
        return "NON DISPONIBILE", "low"
    rate = item.profitable_window_rate
    if item.bets >= 50 and rate >= 0.70:
        return "ALTA", "high"
    if item.bets >= 30 and rate >= 0.60:
        return "BUONA", "medium"
    return "BASE", "low"


def render_live_dashboard(
    candidates: Iterable[LiveCandidate],
    *,
    as_of: str,
    live_status: str = "LIVE AGGIORNATO",
    has_oos: bool = True,
) -> str:
    rows = tuple(candidates)[:5]
    valid = len(rows)
    high = sum(item.confidence >= 0.70 for item in rows)
    medium = sum(0.55 <= item.confidence < 0.70 for item in rows)
    mode = "SPM + OOS" if has_oos else "SPM ONLY"
    cards = []
    for index, item in enumerate(rows, 1):
        home, away = item.fixture
        confidence_class = _confidence_class(item.confidence)
        oos_quality, oos_class = _oos_quality(item, has_oos=has_oos)
        oos_score = f"{item.oos_score:.1f}" if has_oos else "—"
        bets = str(item.bets) if has_oos else "—"
        rate = f"{item.profitable_window_rate:.0%}" if has_oos else "—"
        cards.append(f'''<article class="card {'featured' if index == 1 else ''}">
<header><div class="rank">#{index}</div><div class="label">LIVE PICK</div></header>
<section class="fixture"><div><strong>{escape(home)}</strong><small>CASA</small></div><span class="draw">X</span><div class="away"><strong>{escape(away)}</strong><small>OSPITE</small></div></section>
<div class="confidence-row"><div><small>CONFIDENCE</small><b>{item.confidence:.1%}</b></div><div class="confidence-bar"><span class="{confidence_class}" style="width:{min(max(item.confidence * 100, 0), 100):.1f}%"></span></div></div>
<div class="scores"><div><small>COMBINED</small><b>{item.combined_score:.1f}</b></div><div><small>SPM SCORE</small><b>{item.spm_score:.1f}</b></div><div><small>OOS SCORE</small><b>{oos_score}</b></div><div><small>BET OOS</small><b>{bets}</b></div></div>
<div class="evidence"><span>Qualità OOS <b class="tag {oos_class}">{oos_quality}</b></span><span>Finestre profittevoli <b>{rate}</b></span><span>Segnale <b>PAREGGIO</b></span></div>
</article>''')
    body = ''.join(cards) or '<div class="empty">Nessuna selezione live disponibile</div>'
    return f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>SPM_v2 — Live</title>
<style>:root{{color-scheme:dark;font-family:Inter,system-ui,-apple-system,sans-serif}}*{{box-sizing:border-box}}body{{margin:0;background:#080d18;color:#edf2f7}}main{{max-width:1050px;margin:auto;padding:40px 20px 60px}}.hero{{display:flex;justify-content:space-between;align-items:end;margin-bottom:20px;gap:20px}}h1{{margin:0;font-size:34px;letter-spacing:-.04em}}.sub{{color:#91a0b7;margin-top:7px;font-size:14px}}.status{{display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end}}.date,.status-badge{{border:1px solid #2b3951;border-radius:99px;padding:9px 13px;color:#a9b8cc;font-size:12px;white-space:nowrap}}.status-badge{{color:#9ad7bb;border-color:#385f51}}.summary{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:18px}}.metric{{background:#0e1726;border:1px solid #202e43;border-radius:15px;padding:15px 17px}}.metric small{{display:block;margin-bottom:6px}}.metric b{{font-size:24px}}.metric .hint{{color:#71819a;font-size:11px;margin-left:5px}}.grid{{display:grid;gap:14px}}.card{{background:#101827;border:1px solid #243249;border-radius:20px;padding:20px;box-shadow:0 14px 38px rgba(0,0,0,.18)}}.featured{{border-color:#466487;background:#121e30}}header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:19px}}.rank{{font-weight:800;font-size:16px}}.label{{font-size:10px;letter-spacing:.1em;color:#91a0b7;border:1px solid #30415b;padding:6px 9px;border-radius:99px}}.fixture{{display:grid;grid-template-columns:1fr 44px 1fr;align-items:center;gap:14px;margin-bottom:20px}}.fixture div{{display:flex;flex-direction:column;gap:4px}}.fixture .away{{text-align:right}}.fixture strong{{font-size:20px}}small{{color:#71819a;text-transform:uppercase;font-size:10px;letter-spacing:.07em}}.draw{{width:40px;height:40px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:#1b2b43;color:#c2d1e5;font-weight:900;margin:auto}}.confidence-row{{display:grid;grid-template-columns:auto 1fr;gap:18px;align-items:center;border-top:1px solid #202d42;padding-top:15px}}.confidence-row div:first-child{{display:flex;flex-direction:column;gap:4px;min-width:92px}}.confidence-bar{{height:7px;background:#1c283a;border-radius:99px;overflow:hidden}}.confidence-bar span{{display:block;height:100%;border-radius:99px}}.confidence-bar .high{{background:#65d391}}.confidence-bar .medium{{background:#e1b65a}}.confidence-bar .low{{background:#d47777}}.scores{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;border-top:1px solid #202d42;margin-top:15px;padding-top:15px}}.scores div{{display:flex;flex-direction:column;gap:4px}}.scores b{{font-size:17px}}.evidence{{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-top:15px;color:#91a0b7;font-size:12px}}.evidence b{{color:#cbd6e5}}.tag{{border-radius:99px;padding:4px 8px;font-size:10px;letter-spacing:.04em}}.tag.high{{background:#17382a;color:#76e0a1}}.tag.medium{{background:#3a3019;color:#e5bd62}}.tag.low{{background:#3a2023;color:#e18a8a}}.empty{{padding:45px;text-align:center;color:#91a0b7;border:1px solid #243249;border-radius:20px}}@media(max-width:650px){{main{{padding:25px 12px}}.hero{{align-items:start;flex-direction:column}}.status{{justify-content:flex-start}}.summary{{grid-template-columns:1fr 1fr}}.summary .metric:last-child{{grid-column:1/-1}}.fixture strong{{font-size:17px}}.scores{{grid-template-columns:repeat(2,1fr)}}.evidence{{flex-direction:column;align-items:flex-start}}}}</style></head><body><main><section class="hero"><div><h1>SPM_v2 · Live</h1><div class="sub">Top 5 selezioni basate su {mode}</div></div><div class="status"><div class="status-badge">{escape(live_status)}</div><div class="date">Analisi al {escape(as_of)}</div></div></section><section class="summary"><div class="metric"><small>OPPORTUNITÀ VALIDE</small><b>{valid}</b><span class="hint">/ 5</span></div><div class="metric"><small>CONFIDENCE ≥ 70%</small><b>{high}</b></div><div class="metric"><small>CONFIDENCE 55–69%</small><b>{medium}</b></div></section><section class="grid">{body}</section></main></body></html>'''


def write_live_dashboard(
    candidates: Iterable[LiveCandidate],
    *,
    as_of: str,
    path: str | Path,
    live_status: str = "LIVE AGGIORNATO",
    has_oos: bool = True,
) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        render_live_dashboard(candidates, as_of=as_of, live_status=live_status, has_oos=has_oos),
        encoding="utf-8",
    )
