"""Fast release smoke test for the core SPM_v2 pipeline."""
from pathlib import Path

from spm.backtest.odds_staking import simulate_draw_progression_with_odds
from spm.data.historical_scope import default_historical_scope


def main() -> int:
    scope = default_historical_scope(Path(".historical-cache"))
    assert scope.start_season == "2019-20"
    assert scope.end_season == "2025-26"

    result = simulate_draw_progression_with_odds(
        [("A", False, 2.0), ("A", True, 2.5)],
        initial_bankroll=100.0,
        base_stake=10.0,
    )
    assert result.bets == 2
    assert result.wins == 1
    assert result.final_bankroll == 105.0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
