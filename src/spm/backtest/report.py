"""Serializable backtest reporting primitives."""
from dataclasses import dataclass

from .report_metrics import brier_score, log_loss


@dataclass(frozen=True, slots=True)
class BacktestReport:
    samples: int
    correct: int
    accuracy: float
    brier: float | None = None
    logloss: float | None = None

    @classmethod
    def from_predictions(
        cls,
        actual: list[str],
        predicted: list[str],
        probabilities: list[float] | None = None,
        outcomes: list[int] | None = None,
    ) -> "BacktestReport":
        if len(actual) != len(predicted):
            raise ValueError("actual and predicted must have the same length")
        if (probabilities is None) != (outcomes is None):
            raise ValueError("probabilities and outcomes must be provided together")
        samples = len(actual)
        correct = sum(a == p for a, p in zip(actual, predicted))
        brier = None
        logloss = None
        if probabilities is not None and outcomes is not None:
            if len(probabilities) != samples or len(outcomes) != samples:
                raise ValueError("probabilities and outcomes must match predictions length")
            brier = brier_score(probabilities, outcomes)
            logloss = log_loss(probabilities, outcomes)
        return cls(samples, correct, correct / samples if samples else 0.0, brier, logloss)
