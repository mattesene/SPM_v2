"""Statistical stability diagnostics for OOS SPM selections."""
from __future__ import annotations

from dataclasses import dataclass
from math import sqrt


@dataclass(frozen=True, slots=True)
class StabilityMetrics:
    trials: int
    successes: int
    success_rate: float
    standard_error: float
    lower_95: float
    upper_95: float


def binomial_stability(successes: int, trials: int) -> StabilityMetrics:
    if trials <= 0:
        raise ValueError("trials must be positive")
    if successes < 0 or successes > trials:
        raise ValueError("successes must be between 0 and trials")
    p = successes / trials
    se = sqrt(p * (1.0 - p) / trials)
    # Wald interval, clipped to the probability domain.
    return StabilityMetrics(
        trials=trials,
        successes=successes,
        success_rate=p,
        standard_error=se,
        lower_95=max(0.0, p - 1.96 * se),
        upper_95=min(1.0, p + 1.96 * se),
    )
