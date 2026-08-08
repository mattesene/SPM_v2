"""Evaluation helpers for probability forecasts."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProbabilityMetrics:
    brier_score: float
    log_loss: float


def probability_metrics(probabilities: list[float], outcomes: list[bool]) -> ProbabilityMetrics:
    if not probabilities or len(probabilities) != len(outcomes):
        raise ValueError("probabilities and outcomes must be non-empty and equal length")
    if any(not 0 <= p <= 1 for p in probabilities):
        raise ValueError("probabilities must be in [0, 1]")
    import math
    brier = sum((p - float(y)) ** 2 for p, y in zip(probabilities, outcomes)) / len(outcomes)
    eps = 1e-15
    logloss = -sum(float(y) * math.log(max(p, eps)) + (1 - float(y)) * math.log(max(1 - p, eps)) for p, y in zip(probabilities, outcomes)) / len(outcomes)
    return ProbabilityMetrics(brier, logloss)
