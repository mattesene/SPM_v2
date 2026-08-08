from datetime import date, timedelta

from spm.data.models import Match
from spm.statistics.walk_forward import run_walk_forward


def test_walk_forward_creates_out_of_sample_folds() -> None:
    base = date(2026, 1, 1)
    teams = [("A", "B"), ("B", "C"), ("C", "A")]
    scores = [(1, 1), (2, 0), (0, 1), (1, 0), (0, 0), (2, 1)]
    matches = [
        Match(base + timedelta(days=i), *teams[i % 3], *scores[i % len(scores)])
        for i in range(90)
    ]
    report = run_walk_forward(matches, train_matches=30, test_matches=15, min_history=10, step=0.1)
    assert report.folds
    assert report.mean_test_brier >= 0
    for fold in report.folds:
        assert fold.train_end < fold.test_start
        assert sum(fold.weights) == 1.0
        assert fold.test_predictions > 0
