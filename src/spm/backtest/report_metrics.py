"""Standalone metrics used to evaluate historical draw predictions."""

from __future__ import annotations

from math import log
from typing import Sequence


def _check_lengths(probabilities: Sequence[float], outcomes: Sequence[int]) -> None:
    if len(probabilities) != len(outcomes):
        raise ValueError("probabilities and outcomes must have the same length")


def brier_score(probabilities: Sequence[float], outcomes: Sequence[int]) -> float:
    """Mean squared error of predicted draw probabilities."""
    _check_lengths(probabilities, outcomes)
    if not probabilities:
        return 0.0
    if any(p < 0.0 or p > 1.0 for p in probabilities):
        raise ValueError("probabilities must be between 0 and 1")
    return sum((p - y) ** 2 for p, y in zip(probabilities, outcomes)) / len(probabilities)


def log_loss(probabilities: Sequence[float], outcomes: Sequence[int]) -> float:
    """Binary logarithmic loss with clipping for numerical stability."""
    _check_lengths(probabilities, outcomes)
    if not probabilities:
        return 0.0
    total = 0.0
    for p, y in zip(probabilities, outcomes):
        if y not in (0, 1):
            raise ValueError("outcomes must be binary")
        if p < 0.0 or p > 1.0:
            raise ValueError("probabilities must be between 0 and 1")
        p = min(max(p, 1e-15), 1.0 - 1e-15)
        total -= y * log(p) + (1 - y) * log(1 - p)
    return total / len(probabilities)


def flat_stake_roi(predictions: Sequence[int], outcomes: Sequence[int]) -> float:
    """Return the hit-rate proxy for flat-stake draw selections.

    Real betting ROI requires historical market odds and is intentionally not
    inferred here. This metric is therefore a selection hit-rate proxy.
    """
    _check_lengths(predictions, outcomes)
    bets = sum(1 for prediction in predictions if prediction)
    if bets == 0:
        return 0.0
    wins = sum(1 for prediction, outcome in zip(predictions, outcomes) if prediction and outcome)
    return wins / bets
