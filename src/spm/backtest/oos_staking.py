"""Walk-forward staking using only out-of-sample windows."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .edge_staking import run_edge_staking
from .edge_walk_forward import EdgeWalkForwardWindow
from .market_runner import MarketBacktestObservation


@dataclass(frozen=True, slots=True)
class OOSStakingWindowResult:
    window: EdgeWalkForwardWindow
    selected: int
    bets: int
    profit: float
    final_bankroll: float
    max_drawdown: float


def evaluate_oos_staking_windows(
    observations: Iterable[MarketBacktestObservation],
    thresholds: Iterable[float],
    *,
    train_size: int,
    test_size: int,
    initial_bankroll: float = 1_000.0,
    base_stake: float = 10.0,
) -> tuple[OOSStakingWindowResult, ...]:
    """Calibrate threshold on each train window, stake only on following test data."""
    rows = tuple(observations)
    from .edge_walk_forward import run_edge_walk_forward

    windows = run_edge_walk_forward(
        rows, thresholds, train_size=train_size, test_size=test_size
    )
    results: list[OOSStakingWindowResult] = []
    for window in windows:
        test_rows = rows[window.test_start:window.test_end]
        staking = run_edge_staking(
            test_rows,
            min_edge=window.threshold,
            initial_bankroll=initial_bankroll,
            base_stake=base_stake,
        ).staking
        results.append(OOSStakingWindowResult(
            window=window,
            selected=staking.bets,
            bets=staking.bets,
            profit=staking.profit,
            final_bankroll=staking.final_bankroll,
            max_drawdown=staking.max_drawdown,
        ))
    return tuple(results)
