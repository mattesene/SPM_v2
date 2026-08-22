"""Rank competitions from historical backtest results."""
from __future__ import annotations

from dataclasses import dataclass
from collections import defaultdict

from spm.statistics.competition_report import CompetitionResult


@dataclass(frozen=True, slots=True)
class CompetitionRanking:
    competition: str
    seasons: int
    evaluated: int
    brier_score: float
    actual_draw_rate: float


def rank_competitions(rows: tuple[CompetitionResult, ...]) -> tuple[CompetitionRanking, ...]:
    grouped: dict[str, list[CompetitionResult]] = defaultdict(list)
    for row in rows:
        grouped[row.competition].append(row)

    ranking: list[CompetitionRanking] = []
    for competition, items in grouped.items():
        evaluated = sum(item.evaluated for item in items)
        if evaluated:
            brier = sum(item.brier_score * item.evaluated for item in items) / evaluated
            draw_rate = sum(item.actual_draw_rate * item.evaluated for item in items) / evaluated
        else:
            brier = draw_rate = 0.0
        ranking.append(CompetitionRanking(competition, len(items), evaluated, brier, draw_rate))

    return tuple(sorted(ranking, key=lambda x: (x.brier_score, -x.evaluated, x.competition)))
