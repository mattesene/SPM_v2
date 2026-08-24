from datetime import date

from spm.data.models import Match
from spm.live.selection_evaluation import evaluate_selections, summarize_evaluations
from spm.live.selection_history import LiveSelection


def test_evaluate_settled_draw_and_unplayed_fixture():
    selection = LiveSelection(date(2026, 8, 20), 1, "A", "B", date(2026, 8, 21), .4, 3.0, .8, None, .8)
    evaluations = evaluate_selections([selection], [Match(date(2026, 8, 21), "A", "B", 1, 1)])
    assert evaluations[0].settled
    assert evaluations[0].result == "DRAW"
    assert evaluations[0].profit == 2.0


def test_summary_calculates_roi():
    selection = LiveSelection(date(2026, 8, 20), 1, "A", "B", date(2026, 8, 21), .4, 3.0, .8, None, .8)
    evaluations = evaluate_selections([selection], [Match(date(2026, 8, 21), "A", "B", 1, 1)])
    summary = summarize_evaluations(evaluations)
    assert summary.settled == 1
    assert summary.wins == 1
    assert summary.profit == 2.0
    assert summary.roi == 2.0
