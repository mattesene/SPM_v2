"""Run the historical SPM backtest only when the default dataset scope is complete."""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, is_dataclass
from pathlib import Path

from spm.data.historical_pipeline import prepare_historical_scope
from spm.data.historical_scope import default_historical_scope
from spm.statistics.backtest_runner import run_directory
from spm.statistics.competition_report import build_competition_report
from spm.statistics.competition_ranking import rank_competitions


def _serialize(row):
    return asdict(row) if is_dataclass(row) else row


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path, nargs="?", default=None)
    parser.add_argument("--output", type=Path, default=Path("reports/historical_backtest.json"))
    parser.add_argument("--min-history", type=int, default=1)
    args = parser.parse_args([] if argv is None and "pytest" in Path(sys.argv[0]).name else argv)
    directory = args.directory
    if directory is None:
        scope = default_historical_scope(Path(".historical-cache"))
        prepared = prepare_historical_scope(scope)
        if not prepared.complete:
            raise RuntimeError(f"Historical dataset scope incomplete: {len(prepared.missing)} dataset(s) missing")
        directory = scope.root
    results = run_directory(directory, min_history=args.min_history)
    seasons = build_competition_report(results)
    ranking = rank_competitions(seasons)
    payload = {"datasets": len(results), "seasons": [_serialize(row) for row in seasons], "ranking": [_serialize(row) for row in ranking]}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
