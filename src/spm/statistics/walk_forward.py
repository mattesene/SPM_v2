"""Walk-forward validation for SPM calibration.

Training and evaluation windows are strictly chronological. Calibration is
performed only on the training window and the resulting weights are evaluated
on the following test window.
"""

from dataclasses import dataclass
from datetime import date

from spm.data.models import Match
from spm.statistics.calibration import calibrate_weights
from spm.statistics.engine import SPMEngine


@dataclass(frozen=True, slots=True)
class FoldResult:
    train_end: date
    test_start: date
    test_end: date
    weights: tuple[float, ...]
    train_brier: float
    test_brier: float
    test_predictions: int


@dataclass(frozen=True, slots=True)
class WalkForwardReport:
    folds: tuple[FoldResult, ...]
    mean_test_brier: float
    mean_train_brier: float


def run_walk_forward(
    matches: list[Match],
    train_matches: int = 50,
    test_matches: int = 20,
    min_history: int = 10,
    step: float = 0.05,
) -> WalkForwardReport:
    ordered = sorted(matches, key=lambda m: m.date)
    if train_matches < min_history or test_matches < 1:
        raise ValueError("invalid train/test window")

    folds: list[FoldResult] = []
    start = 0
    while start + train_matches < len(ordered):
        train = ordered[start : start + train_matches]
        test = ordered[start + train_matches : start + train_matches + test_matches]
        if not test:
            break

        features: list[tuple[float, float, float, float]] = []
        outcomes: list[bool] = []
        for i, match in enumerate(train):
            history = train[:i]
            if len(history) < min_history:
                continue
            try:
                result = SPMEngine().score(history, match.home_team, match.away_team, match.date)
            except ValueError:
                continue
            features.append((result.draw_probability, result.form_balance, result.draw_signal, result.goal_balance_signal))
            outcomes.append(match.is_draw)

        if not features:
            start += test_matches
            continue

        calibration = calibrate_weights(features, outcomes, step=step)
        test_errors: list[float] = []
        for offset, match in enumerate(test):
            # The complete history available at this point is the training
            # window plus only earlier matches from the current test window.
            history = ordered[: start + train_matches + offset]
            if len(history) < min_history:
                continue
            try:
                result = SPMEngine().score(history, match.home_team, match.away_team, match.date)
            except ValueError:
                continue
            vector = (result.draw_probability, result.form_balance, result.draw_signal, result.goal_balance_signal)
            probability = sum(x * w for x, w in zip(vector, calibration.weights))
            test_errors.append((probability - float(match.is_draw)) ** 2)

        if test_errors:
            folds.append(FoldResult(train[-1].date, test[0].date, test[-1].date, calibration.weights, calibration.brier_score, sum(test_errors) / len(test_errors), len(test_errors)))
        start += test_matches

    mean_test = sum(f.test_brier for f in folds) / len(folds) if folds else 0.0
    mean_train = sum(f.train_brier for f in folds) / len(folds) if folds else 0.0
    return WalkForwardReport(tuple(folds), mean_test, mean_train)
