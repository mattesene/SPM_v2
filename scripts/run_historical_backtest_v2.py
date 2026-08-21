"""Run the historical SPM backtest and emit a compact machine-readable report."""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from spm.statistics.backtest_runner import run_directory
from spm.statistics.competition_report import build_competition_report
from spm.statistics.competition_ranking import rank_competitions


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    parser.add_argument("--output", type=Path, default=Path("reports/historical_backtest.json"))
    parser.add_argument("--min-history", type=int, default=1)
    args = parser.parse_args()

    results = run_directory(args.directory, min_history=args.min_history)
    seasons = build_competition_report(results)
    ranking = rank_competitions(seasons)
    payload = {
        "datasets": len(results),
        "seasons": [asdict(row) for row in seasons],
        "ranking": [asdict(row) for row in ranking],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
