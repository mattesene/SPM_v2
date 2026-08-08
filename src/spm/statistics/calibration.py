"""Deterministic weight calibration for SPM features.

The optimizer uses only training predictions supplied by a caller. It searches
simple simplex weights, minimizing Brier score, and is intentionally small and
reproducible so it can later be replaced by a richer optimizer without
changing the public API.
"""

from dataclasses import dataclass
from itertools import product


@dataclass(frozen=True, slots=True)
class CalibrationResult:
    weights: tuple[float, ...]
    brier_score: float


def calibrate_weights(features: list[tuple[float, ...]], outcomes: list[bool], step: float = 0.05) -> CalibrationResult:
    if not features or len(features) != len(outcomes):
        raise ValueError("features and outcomes must be non-empty and have equal length")
    width = len(features[0])
    if width == 0 or any(len(row) != width for row in features):
        raise ValueError("all feature rows must have equal non-zero width")
    if not 0 < step <= 1:
        raise ValueError("step must be in (0, 1]")

    units = round(1 / step)
    best = CalibrationResult(tuple([1 / width] * width), float("inf"))
    for integer_weights in _compositions(units, width):
        weights = tuple(value / units for value in integer_weights)
        score = _brier(features, outcomes, weights)
        if score < best.brier_score:
            best = CalibrationResult(weights, score)
    return best


def _compositions(total: int, width: int):
    if width == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in _compositions(total - first, width - 1):
            yield (first, *rest)


def _brier(features, outcomes, weights) -> float:
    return sum((sum(x * w for x, w in zip(row, weights)) - float(y)) ** 2 for row, y in zip(features, outcomes)) / len(outcomes)
