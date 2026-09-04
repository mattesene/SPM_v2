from datetime import date

import pytest

from spm.backtest.calibration import build_calibration
from spm.backtest.team_progression import TeamProgressionObservation


def _row(probability: float, streak: int, draw: bool) -> TeamProgressionObservation:
    return TeamProgressionObservation(
        date(2026, 1, 1), "Team", "Opponent", probability, streak, draw, 1 << streak
    )


def test_calibration_report_exposes_gap_and_wilson_interval() -> None:
    report = build_calibration([
        _row(0.60, 0, True),
        _row(0.60, 0, False),
        _row(0.80, 1, True),
        _row(0.80, 1, True),
    ])

    assert report["overall_observed_draw_rate"] == pytest.approx(0.75)
    assert report["overall_observed_rate_ci95_low"] < 0.75
    assert report["overall_observed_rate_ci95_high"] > 0.75
    assert report["mean_absolute_calibration_gap"] == pytest.approx(0.35)

    first = report["probability_buckets"][0]
    assert first["calibration_gap"] == pytest.approx(0.10)
    assert 0.0 <= first["observed_rate_ci95_low"] <= first["observed_rate_ci95_high"] <= 1.0


def test_empty_calibration_report_is_safe() -> None:
    report = build_calibration([])
    assert report["overall_observed_draw_rate"] == 0.0
    assert report["overall_observed_rate_ci95_low"] == 0.0
    assert report["overall_observed_rate_ci95_high"] == 0.0
    assert report["mean_absolute_calibration_gap"] == 0.0
    assert report["streak_buckets"] == []
    assert report["probability_buckets"] == []
