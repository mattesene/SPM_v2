"""Group out-of-sample walk-forward results by market dimensions."""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Callable, Iterable

from .oos_staking import OOSStakingWindowResult


@dataclass(frozen=True, slots=True)
class OOSGroupResult:
    key: str
    windows: int
    bets: int
    profit: float
    roi: float
    max_drawdown: float
    profitable_windows: int


def aggregate_oos_by_group(
    rows: Iterable[tuple[OOSStakingWindowResult, object]],
    *,
    key_fn: Callable[[object], object],
    initial_bankroll: float = 1_000.0,
) -> tuple[OOSGroupResult, ...]:
    groups: dict[str, list[OOSStakingWindowResult]] = defaultdict(list)
    for result, observation in rows:
        groups[str(key_fn(observation))].append(result)
    output: list[OOSGroupResult] = []
    for key in sorted(groups):
        items = groups[key]
        profit = sum(item.profit for item in items)
        output.append(OOSGroupResult(
            key=key,
            windows=len(items),
            bets=sum(item.bets for item in items),
            profit=profit,
            roi=profit / initial_bankroll if initial_bankroll else 0.0,
            max_drawdown=max((item.max_drawdown for item in items), default=0.0),
            profitable_windows=sum(item.profit > 0 for item in items),
        ))
    return tuple(output)
