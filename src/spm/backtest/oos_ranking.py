"""Rank entities by out-of-sample market performance."""
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .oos_staking import OOSStakingWindowResult


@dataclass(frozen=True, slots=True)
class OOSRankingEntry:
    key: str
    windows: int
    bets: int
    profit: float
    roi: float
    max_drawdown: float
    profitable_window_rate: float
    score: float


def rank_oos_results(
    rows: Iterable[tuple[OOSStakingWindowResult, object]],
    *,
    key_fn,
    initial_bankroll: float = 1_000.0,
    min_bets: int = 1,
) -> tuple[OOSRankingEntry, ...]:
    """Rank by risk-adjusted OOS performance, not raw historical draw rate."""
    if initial_bankroll <= 0:
        raise ValueError("initial_bankroll must be positive")
    if min_bets < 0:
        raise ValueError("min_bets cannot be negative")
    groups: dict[str, list[OOSStakingWindowResult]] = {}
    for result, observation in rows:
        key = str(key_fn(observation))
        groups.setdefault(key, []).append(result)

    output: list[OOSRankingEntry] = []
    for key, items in groups.items():
        bets = sum(item.bets for item in items)
        if bets < min_bets:
            continue
        profit = sum(item.profit for item in items)
        roi = profit / initial_bankroll
        drawdown = max((item.max_drawdown for item in items), default=0.0)
        profitable_rate = sum(item.profit > 0 for item in items) / len(items)
        score = roi - (drawdown / initial_bankroll) + 0.25 * profitable_rate
        output.append(OOSRankingEntry(key, len(items), bets, profit, roi, drawdown, profitable_rate, score))
    return tuple(sorted(output, key=lambda row: (-row.score, row.key)))


def load_oos_ranking(path: str | Path) -> tuple[OOSRankingEntry, ...]:
    """Load a previously generated OOS ranking CSV.

    Missing files are treated as an empty ranking so Live can still publish the
    SPM-only layer while OOS calibration is being refreshed.
    """
    source = Path(path)
    if not source.is_file():
        return ()
    entries: list[OOSRankingEntry] = []
    with source.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            try:
                entries.append(
                    OOSRankingEntry(
                        key=row["key"],
                        windows=int(row["windows"]),
                        bets=int(row["bets"]),
                        profit=float(row["profit"]),
                        roi=float(row["roi"]),
                        max_drawdown=float(row["max_drawdown"]),
                        profitable_window_rate=float(row["profitable_window_rate"]),
                        score=float(row["score"]),
                    )
                )
            except (KeyError, TypeError, ValueError) as exc:
                raise ValueError(f"invalid OOS ranking row in {source}") from exc
    return tuple(entries)
