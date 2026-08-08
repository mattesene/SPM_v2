"""Probability utilities for match outcomes."""

from math import isclose


def draw_rate(draws: int, matches: int) -> float:
    """Return the empirical draw probability.

    Raises ValueError for invalid counts instead of silently returning a
    misleading value.
    """
    if matches <= 0:
        raise ValueError("matches must be greater than zero")
    if draws < 0 or draws > matches:
        raise ValueError("draws must be between zero and matches")
    return draws / matches


def poisson_pmf(k: int, lam: float) -> float:
    """Return P(X=k) for a Poisson variable with rate ``lam``."""
    if k < 0 or int(k) != k:
        raise ValueError("k must be a non-negative integer")
    if lam < 0:
        raise ValueError("lambda must be non-negative")
    if lam == 0:
        return 1.0 if k == 0 else 0.0

    # Iterative form avoids requiring scipy for the core model.
    probability = 1.0
    for i in range(1, k + 1):
        probability *= lam / i
    probability *= __import__("math").exp(-lam)
    return probability


def approximately_probability(value: float) -> bool:
    """Validate that a scalar is numerically within [0, 1]."""
    return -1e-12 <= value <= 1 + 1e-12
