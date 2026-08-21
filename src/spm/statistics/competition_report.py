"""Competition/season level historical backtest reporting."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from spm.statistics.backtest_runner import DatasetBacktest, run_directory


@dataclass(frozen=True, slots=True)
class CompetitionResult:
    competition: str
    season: str
    dataset: str
    evaluated: int
    skipped: int
    brier_score: float
    actual_draw_rate: float


def _parse_dataset(name: str) -> tuple[str, str]:
    stem = Path(name).stem
    match = re.match(r"(.+?)[_-](\d{4})[_-](\d{2,4})$", stem)
    if match:
        competition, start, end = match.groups()
        return competition, f"{start}/{end[-2:]}"
    return stem, "unknown"


def build_competition_report(results: tuple[DatasetBacktest, ...]) -> tuple[CompetitionResult, ...]:
    rows: list[CompetitionResult] = []
    for item in results:
        competition, season = _parse_dataset(item.dataset)
        rows.append(CompetitionResult(
            competition=competition,
            season=season,
            dataset=item.dataset,
            evaluated=item.summary.evaluated,
            skipped=item.summary.skipped,
            brier_score=item.summary.brier_score,
            actual_draw_rate=item.summary.actual_draw_rate,
        ))
    return tuple(rows)


def run_competition_report(directory: str | Path, *, min_history: int = 1) -> tuple[CompetitionResult, ...]:
    return build_competition_report(run_directory(directory, min_history=min_history))
