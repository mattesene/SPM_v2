"""Evaluate matured Live selections against completed match results."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Iterable

from spm.data.models import Match
from spm.live.selection_history import LiveSelection

@dataclass(frozen=True, slots=True)
class SelectionEvaluation:
    selection: LiveSelection
    result: str | None
    settled: bool
    profit: float | None

@dataclass(frozen=True, slots=True)
class EvaluationSummary:
    settled: int
    wins: int
    losses: int
    pushes: int
    profit: float
    roi: float | None

def _result(match: Match) -> str:
    if match.home_goals == match.away_goals:
        return "DRAW"
    return "HOME" if match.home_goals > match.away_goals else "AWAY"

def evaluate_selections(selections: Iterable[LiveSelection], matches: Iterable[Match]) -> tuple[SelectionEvaluation, ...]:
    by_key = {(m.date, m.home_team.strip(), m.away_team.strip()): m for m in matches}
    result = []
    for selection in selections:
        match = by_key.get((selection.fixture_date, selection.home_team.strip(), selection.away_team.strip()))
        if match is None:
            result.append(SelectionEvaluation(selection, None, False, None))
            continue
        won = _result(match) == "DRAW"
        odds = selection.draw_odds
        profit = (odds - 1.0) if won and odds is not None else (-1.0 if odds is not None else None)
        result.append(SelectionEvaluation(selection, _result(match), True, profit))
    return tuple(result)

def summarize_evaluations(evaluations: Iterable[SelectionEvaluation]) -> EvaluationSummary:
    settled = [e for e in evaluations if e.settled]
    wins = sum(e.profit is not None and e.profit > 0 for e in settled)
    losses = sum(e.profit is not None and e.profit < 0 for e in settled)
    pushes = sum(e.profit == 0 for e in settled)
    profit = sum(e.profit or 0.0 for e in settled)
    stake = sum(1.0 for e in settled if e.profit is not None)
    return EvaluationSummary(len(settled), wins, losses, pushes, profit, profit / stake if stake else None)
