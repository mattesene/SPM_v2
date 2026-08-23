from pathlib import Path

from spm.backtest.live_report import build_live_report
from spm.backtest.oos_ranking import OOSRankingEntry
from spm.statistics.engine import SPMScore


def test_build_live_report_renders_selected_top5(tmp_path: Path) -> None:
    scores = [SPMScore(f"H{i}", f"A{i}", .30, 30.0 - i, .8, .8, .8, (.6, .15, .15, .1)) for i in range(6)]
    evidence = [OOSRankingEntry(f"H{i} vs A{i}", 20, 100.0 - i, .10, .80, 0, 0, 0) for i in range(6)]
    output = tmp_path / "live.html"
    selected = build_live_report(scores, evidence, as_of="2026-08-23", path=output)
    assert len(selected) == 5
    html = output.read_text(encoding="utf-8")
    assert "SPM_v2 · Live" in html
    assert "Combined" in html
    assert "Confidence" in html
    assert "OPPORTUNITÀ VALIDE" in html
    assert "CONFIDENCE ≥ 70%" in html
    assert html.count('class="card') == 5
