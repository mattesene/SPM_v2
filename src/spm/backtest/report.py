"""Serializable backtest reporting primitives."""
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BacktestReport:
    samples: int
    correct: int
    accuracy: float

    @classmethod
    def from_predictions(cls, actual: list[str], predicted: list[str]) -> "BacktestReport":
        if len(actual) != len(predicted):
            raise ValueError("actual and predicted must have the same length")
        samples = len(actual)
        correct = sum(a == p for a, p in zip(actual, predicted))
        return cls(samples, correct, correct / samples if samples else 0.0)
