"""Calibration and streak diagnostics for team-first backtest observations."""
from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from dataclasses import asdict, dataclass

from spm.backtest.team_progression import TeamProgressionObservation


@dataclass(frozen=True, slots=True)
class CalibrationBucket:
    label: str
    count: int
    predicted_probability: float
    observed_draw_rate: float
    brier_score: float


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
        observed = sum(r.actual_draw for r in group) / len(group)
        predicted = sum(r.selected_probability for r in group) / len(group)
        brier = sum((r.selected_probability - int(r.actual_draw)) ** 2 for r in group) / len(group)
        return CalibrationBucket(label, len(group), predicted, observed, brier)

    streaks = [asdict(bucket(str(streak), group)) for streak, group in sorted(streak_groups.items())]
    probabilities = [asdict(bucket(label, group)) for label, group in sorted(probability_groups.items(), key=lambda item: int(item[0].split("-")[0]))]
    overall = sum(r.actual_draw for r in rows) / len(rows) if rows else 0.0
    return {
        "overall_observed_draw_rate": overall,
        "streak_buckets": streaks,
        "probability_buckets": probabilities,
    }
