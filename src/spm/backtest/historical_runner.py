"""Run chronological historical backtests, including market-aware staking."""
from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from spm.backtest.engine import ChronologicalBacktester
from spm.backtest.market_runner import MarketBacktestObservation, run_market_backtest
from spm.backtest.odds_staking import OddsStakingResult
from spm.data.default_historical_catalog import default_catalog
from spm.data.historical_ingest import ingest_catalog
from spm.data.historical_odds import load_historical_draw_odds
from spm.data.normalized import MatchRecord
from spm.ingestion.backtest_input import to_backtest_matches


def run_historical_backtest(
    records: Iterable[MatchRecord],
    *,
    min_history: int = 3,
):
    """Convert validated records and execute the leakage-safe backtester."""
    matches = to_backtest_matches(records)
    return ChronologicalBacktester(min_history=min_history).run(matches)


def run_default_catalog_backtest(root: str | Path, *, min_history: int = 3):
    """Ingest the complete V1 catalog and run the leakage-safe backtest."""
    catalog = default_catalog()
    ingestion = ingest_catalog(catalog, root)
    records = [record for dataset in ingestion.datasets.values() for record in dataset]
    return run_historical_backtest(records, min_history=min_history)


def run_default_catalog_market_backtest(
    root: str | Path,
    *,
    min_history: int = 3,
    threshold: float = 0.0,
    min_streak: int = 0,
    min_edge: float = 0.0,
    initial_bankroll: float = 1_000.0,
    base_stake: float = 10.0,
) -> tuple[tuple[MarketBacktestObservation, ...], OddsStakingResult]:
    """Run the complete V1 catalog through SPM and actual historical draw prices."""
    catalog = default_catalog()
    ingestion = ingest_catalog(catalog, root)
    records = [record for dataset in ingestion.datasets.values() for record in dataset]
    matches = to_backtest_matches(records)
    odds = load_historical_draw_odds(catalog, root)
    return run_market_backtest(
        matches,
        odds,
        min_history=min_history,
        threshold=threshold,
        min_streak=min_streak,
        min_edge=min_edge,
        initial_bankroll=initial_bankroll,
        base_stake=base_stake,
    )
