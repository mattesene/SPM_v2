"""Run the complete historical SPM draw strategy with market draw prices."""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from spm.backtest.historical_runner import run_default_catalog_market_backtest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    parser.add_argument("--output", type=Path, default=Path("reports/historical_market_backtest.json"))
    parser.add_argument("--min-history", type=int, default=3)
    parser.add_argument("--min-streak", type=int, default=3)
    parser.add_argument("--min-edge", type=float, default=0.0)
    parser.add_argument("--initial-bankroll", type=float, default=1000.0)
    parser.add_argument("--base-stake", type=float, default=10.0)
    args = parser.parse_args()

    observations, staking = run_default_catalog_market_backtest(
        args.directory,
        min_history=args.min_history,
        min_streak=args.min_streak,
        min_edge=args.min_edge,
        initial_bankroll=args.initial_bankroll,
        base_stake=args.base_stake,
    )
    selected = [item for item in observations if item.selected]
    with_odds = [item for item in selected if item.draw_odds is not None]
    payload = {
        "parameters": {
            "min_history": args.min_history,
            "min_streak": args.min_streak,
            "min_edge": args.min_edge,
            "initial_bankroll": args.initial_bankroll,
            "base_stake": args.base_stake,
        },
        "observations": len(observations),
        "selected": len(selected),
        "selected_with_odds": len(with_odds),
        "staking": asdict(staking),
        "selected_matches": [asdict(item) for item in with_odds],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
