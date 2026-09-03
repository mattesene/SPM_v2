"""Apply SPM staking to catalog outcomes, optionally using match-level odds."""
from __future__ import annotations

from dataclasses import dataclass

from .odds_staking import OddsStakingResult, simulate_draw_progression_with_odds
from .staking import StakingResult, simulate_draw_progression


@dataclass(frozen=True, slots=True)
class CatalogStakingResult:
    datasets: int
    observations: int
    draw_rate: float
    staking: StakingResult


@dataclass(frozen=True, slots=True)
class CatalogOddsStakingResult:
    datasets: int
    observations: int
    selected: int
    draw_rate: float
    staking: OddsStakingResult


def run_catalog_staking(
    outcomes_by_dataset: dict[str, list[bool]],
    *,
    initial_bankroll: float = 1_000.0,
    base_stake: float = 10.0,
    payout_odds: float = 3.0,
) -> CatalogStakingResult:
    outcomes: list[bool] = []
    for dataset in sorted(outcomes_by_dataset):
        outcomes.extend(outcomes_by_dataset[dataset])
    observations = len(outcomes)
    draw_rate = sum(outcomes) / observations if observations else 0.0
    staking = simulate_draw_progression(outcomes, initial_bankroll=initial_bankroll, base_stake=base_stake, payout_odds=payout_odds)
    return CatalogStakingResult(len(outcomes_by_dataset), observations, draw_rate, staking)


def run_catalog_odds_staking(
    selections_by_dataset: dict[str, list[tuple]],
    *,
    initial_bankroll: float = 1_000.0,
    base_stake: float = 10.0,
) -> CatalogOddsStakingResult:
    """Backtest catalog rows, accepting both legacy and explicit team rows."""
    selections: list[tuple[str, bool, float | None]] = []
    for dataset in sorted(selections_by_dataset):
        for row in selections_by_dataset[dataset]:
            if len(row) == 2:
                is_draw, odds = row
                selections.append((dataset, is_draw, odds))
            elif len(row) == 3:
                team, is_draw, odds = row
                selections.append((team, is_draw, odds))
            else:
                raise ValueError("catalog selection rows must contain 2 or 3 values")
    observations = len(selections)
    priced = [row for row in selections if row[2] is not None]
    selected = len(priced)
    draw_rate = sum(is_draw for _, is_draw, odds in priced if odds is not None) / selected if selected else 0.0
    staking = simulate_draw_progression_with_odds(selections, initial_bankroll=initial_bankroll, base_stake=base_stake)
    return CatalogOddsStakingResult(len(selections_by_dataset), observations, selected, draw_rate, staking)
