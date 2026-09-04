"""Calibration and streak diagnostics for team-first backtest observations."""
from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from math import sqrt

from spm.backtest.team_progression import TeamProgressionObservation


@dataclass(frozen=True, slots=True)
class CalibrationBucket:
    label: str
    count: int
    predicted_probability: float
    observed_draw_rate: float
    brier_score: float
    calibration_gap: float
    observed_rate_ci95_low: float
    observed_rate_ci95_high: float


def _wilson_interval(successes: int, total: int, z: float = 1.96) -> tuple[float, float]:
    """Return a bounded Wilson score interval for a binomial proportion."""
    if total <= 0:
        return 0.0, 0.0
    p = successes / total
    denominator = 1.0 + z * z / total
    centre = (p + z * z / (2.0 * total)) / denominator
    margin = z * sqrt((p * (1.0 - p) / total) + (z * z / (4.0 * total * total))) / denominator
    return max(0.0, centre - margin), min(1.0, centre + margin)


def build_calibration(observations: Iterable[TeamProgressionObservation]) -> dict[str, object]:
    rows = list(observations)
    streak_groups: dict[int, list[TeamProgressionObservation]] = defaultdict(list)
    probability_groups: dict[str, list[TeamProgressionObservation]] = defaultdict(list)
    for row in rows:
        streak_groups[row.streak_before].append(row)
        lower = min(int(row.selected_probability * 10) * 10, 90)
        label = f"{lower}-{lower + 10}%"
        probability_groups[label].append(row)

    def bucket(label: str, group: list[TeamProgressionObservation]) -> CalibrationBucket:
        count = len(group)
        draws = sum(r.actual_draw for r in group)
        observed = draws / count
        predicted = sum(r.selected_probability for r in group) / count
        brier = sum((r.selected_probability - int(r.actual_draw)) ** 2 for r in group) / count
        low, high = _wilson_interval(draws, count)
        return CalibrationBucket(
            label,
            count,
            predicted,
            observed,
            brier,
            abs(predicted - observed),
            low,
            high,
        )

    streaks = [asdict(bucket(str(streak), group)) for streak, group in sorted(streak_groups.items())]
    probabilities = [asdict(bucket(label, group)) for label, group in sorted(probability_groups.items(), key=lambda item: int(item[0].split("-")[0]))]
    overall = sum(r.actual_draw for r in rows) / len(rows) if rows else 0.0
    overall_low, overall_high = _wilson_interval(sum(r.actual_draw for r in rows), len(rows))
    mean_gap = (
        sum(abs(r.selected_probability - int(r.actual_draw)) for r in rows) / len(rows)
        if rows else 0.0
    )
    return {
        "overall_observed_draw_rate": overall,
        "overall_observed_rate_ci95_low": overall_low,
        "overall_observed_rate_ci95_high": overall_high,
        "mean_absolute_calibration_gap": mean_gap,
        "streak_buckets": streaks,
        "probability_buckets": probabilities,
    }
