"""Leakage-safe historical backtesting for SPM predictions."""

from dataclasses import dataclass
from datetime import date
from math import log

from spm.data.models import Match
from spm.statistics.engine import SPMEngine


@dataclass(frozen=True, slots=True)
class BacktestPrediction:
    date: date
    home_team: str
    away_team: str
    probability: float
    predicted_draw: bool
    actual_draw: bool
    brier_error: float


@dataclass(frozen=True, slots=True)
class BacktestReport:
    predictions: tuple[BacktestPrediction, ...]
    accuracy: float
    precision: float
    recall: float
    f1: float
    brier_score: float
    baseline_brier_score: float
    roi: float


class Backtester:
    """Evaluate SPM chronologically without using future matches."""

    def __init__(self, threshold: float = 0.33) -> None:
        if not 0 < threshold < 1:
            raise ValueError("threshold must be between 0 and 1")
        self.threshold = threshold

    def run(self, matches: list[Match], min_history: int = 10) -> BacktestReport:
        ordered = sorted(matches, key=lambda m: m.date)
        predictions: list[BacktestPrediction] = []
        draws = 0
        correct = true_positive = false_positive = false_negative = 0
        roi_profit = 0.0
        bets = 0

        for index, match in enumerate(ordered):
            history = ordered[:index]
            if len(history) < min_history:
                continue
            teams = {m.home_team for m in history} | {m.away_team for m in history}
            if match.home_team not in teams or match.away_team not in teams:
                continue
            try:
                result = SPMEngine().score(history, match.home_team, match.away_team, match.date)
            except ValueError:
                continue

            actual = match.is_draw
            predicted = result.draw_probability >= self.threshold
            if predicted == actual:
                correct += 1
            if predicted and actual:
                true_positive += 1
            elif predicted and not actual:
                false_positive += 1
            elif not predicted and actual:
                false_negative += 1
            draws += actual

            # Calibration metric: squared probability error.
            error = (result.draw_probability - float(actual)) ** 2
            predictions.append(BacktestPrediction(match.date, match.home_team, match.away_team, result.draw_probability, predicted, actual, error))

            # Optional flat-stake simulation: bet only when model probability
            # exceeds the threshold. A fair odds proxy is used here; real odds
            # ingestion belongs to the market-data milestone.
            if predicted:
                bets += 1
                roi_profit += 1.0 if actual else -1.0

        n = len(predictions)
        accuracy = correct / n if n else 0.0
        precision = true_positive / (true_positive + false_positive) if true_positive + false_positive else 0.0
        recall = true_positive / (true_positive + false_negative) if true_positive + false_negative else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        brier = sum(p.brier_error for p in predictions) / n if n else 0.0
        baseline = draws / n if n else 0.0
        baseline_brier = sum((baseline - float(p.actual_draw)) ** 2 for p in predictions) / n if n else 0.0
        roi = roi_profit / bets if bets else 0.0
        return BacktestReport(tuple(predictions), accuracy, precision, recall, f1, brier, baseline_brier, roi)
