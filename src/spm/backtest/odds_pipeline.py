"""End-to-end adapter from OOS observations to odds-aware catalog staking."""
from __future__ import annotations

from dataclasses import dataclass

from spm.data.odds import DrawOdds
from .catalog_staking import CatalogOddsStakingResult, run_catalog_odds_staking
from .engine import BacktestObservation
from .odds_adapter import attach_odds_to_oos


@dataclass(frozen=True, slots=True)
class OOSOddsPipelineResult:
    selections_by_dataset: dict[str, list[tuple[bool, float | None]]]
    staking: CatalogOddsStakingResult


def run_oos_odds_pipeline(
    observations_by_dataset: dict[str, list[BacktestObservation]],
    odds: list[DrawOdds],
    *,
    initial_bankroll: float = 1_000.0,
    base_stake: float = 10.0,
) -> OOSOddsPipelineResult:
    selections_by_dataset: dict[str, list[tuple[bool, float | None]]] = {}
    for dataset in sorted(observations_by_dataset):
        attached = attach_odds_to_oos(observations_by_dataset[dataset], odds)
        selections_by_dataset[dataset] = [
            (item.is_draw, item.draw_odds) for item in attached if item.selected
        ]
    staking = run_catalog_odds_staking(
        selections_by_dataset,
        initial_bankroll=initial_bankroll,
        base_stake=base_stake,
    )
    return OOSOddsPipelineResult(selections_by_dataset, staking)
