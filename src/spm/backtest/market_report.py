"""Reporting helpers for the end-to-end SPM market backtest."""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from typing import Callable, Iterable

from .market_runner import MarketBacktestObservation
from .odds_staking import OddsStakingResult


@dataclass(frozen=True, slots=True)
class MarketGroupReport:
    key: str
    observations: int
    selected: int
    priced: int
    draws: int
    draw_rate: float
    priced_draw_rate: float
    selection_rate: float


def build_market_group_report(
    observations: Iterable[MarketBacktestObservation],
    *,
    key_fn: Callable[[MarketBacktestObservation], object],
) -> tuple[MarketGroupReport, ...]:
    groups: dict[str, list[MarketBacktestObservation]] = defaultdict(list)
    for observation in observations:
        groups[str(key_fn(observation))].append(observation)
    reports: list[MarketGroupReport] = []
    for key in sorted(groups):
        rows = groups[key]
        selected = [row for row in rows if row.selected]
        priced = [row for row in selected if row.draw_odds is not None]
        draws = sum(row.actual_draw for row in rows)
        priced_draws = sum(row.actual_draw for row in priced)
        reports.append(MarketGroupReport(
            key=key,
            observations=len(rows),
            selected=len(selected),
            priced=len(priced),
            draws=draws,
            draw_rate=draws / len(rows) if rows else 0.0,
            priced_draw_rate=priced_draws / len(priced) if priced else 0.0,
            selection_rate=len(selected) / len(rows) if rows else 0.0,
        ))
    return tuple(reports)


def group_by_season(observation: MarketBacktestObservation) -> str:
    return str(observation.date.year)


def group_by_team(observation: MarketBacktestObservation) -> str:
    return observation.home_team


def group_by_match_date(observation: MarketBacktestObservation) -> date:
    return observation.date


def staking_summary(result: OddsStakingResult) -> dict[str, float | int]:
    roi = result.profit / result.max_exposure if result.max_exposure else 0.0
    win_rate = result.wins / result.bets if result.bets else 0.0
    return {
        "final_bankroll": result.final_bankroll,
        "profit": result.profit,
        "roi_on_max_exposure": roi,
        "max_drawdown": result.max_drawdown,
        "max_exposure": result.max_exposure,
        "bets": result.bets,
        "wins": result.wins,
        "win_rate": win_rate,
        "skipped": result.skipped,
    }
