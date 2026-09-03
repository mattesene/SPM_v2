"""Run the leakage-safe same-team draw progression over the full historical scope."""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

from spm.backtest.team_progression import run_team_progression_backtest
from spm.data.csv import CSVMatchImporter
from spm.data.historical_pipeline import prepare_historical_scope
from spm.data.historical_scope import default_historical_scope


def _summary(report):
    streaks = [row.streak_before for row in report.observations]
    return {
        "bets": report.bets,
        "draws": report.draws,
        "non_draws": report.non_draws,
        "hit_rate": report.hit_rate,
        "teams_selected": report.teams_selected,
        "series_started": report.series_started,
        "series_completed": report.series_completed,
        "completion_rate": report.completion_rate,
        "max_streak": report.max_streak,
        "avg_streak_before": sum(streaks) / len(streaks) if streaks else 0.0,
        "max_stake_units": report.max_stake_units,
        "max_capital_units": report.max_capital_units,
        "busts": report.busts,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache", type=Path, default=Path(".historical-cache"))
    parser.add_argument("--output", type=Path, default=Path("reports/team_progression_backtest.json"))
    parser.add_argument("--min-history", type=int, default=5)
    parser.add_argument("--top-n", type=int, default=5)
    args = parser.parse_args()

    scope = default_historical_scope(args.cache)
    prepared = prepare_historical_scope(scope)
    if not prepared.complete:
        raise RuntimeError(f"Historical dataset scope incomplete: {len(prepared.missing)} dataset(s) missing")

    importer = CSVMatchImporter()
    datasets = []
    aggregate = defaultdict(int)
    team_stats = defaultdict(lambda: {"bets": 0, "draws": 0, "series_started": 0, "series_completed": 0, "max_streak": 0, "max_stake_units": 0})

    for path in sorted(scope.root.rglob("*.csv")):
        matches = importer.load(path)
        report = run_team_progression_backtest(matches, min_history=args.min_history, top_n=args.top_n)
        summary = _summary(report)
        datasets.append({"dataset": str(path.relative_to(scope.root)), "matches": len(matches), **summary})
        aggregate["matches"] += len(matches)
        for key in ("bets", "draws", "non_draws", "teams_selected", "series_started", "series_completed"):
            aggregate[key] += summary[key]
        aggregate["max_streak"] = max(aggregate["max_streak"], summary["max_streak"])
        aggregate["max_stake_units"] = max(aggregate["max_stake_units"], summary["max_stake_units"])
        aggregate["max_capital_units"] = max(aggregate["max_capital_units"], summary["max_capital_units"])
        aggregate["busts"] += summary["busts"]
        for row in report.observations:
            key = (path.name, row.team)
            stats = team_stats[key]
            stats["bets"] += 1
            stats["draws"] += int(row.actual_draw)
            stats["max_streak"] = max(stats["max_streak"], row.streak_before)
            stats["max_stake_units"] = max(stats["max_stake_units"], row.stake_units)
            if row.streak_before == 0:
                stats["series_started"] += 1
            if row.actual_draw:
                stats["series_completed"] += 1

    aggregate["hit_rate"] = aggregate["draws"] / aggregate["bets"] if aggregate["bets"] else 0.0
    aggregate["completion_rate"] = aggregate["series_completed"] / aggregate["series_started"] if aggregate["series_started"] else 0.0
    aggregate["dataset_count"] = len(datasets)
    aggregate["min_history"] = args.min_history
    aggregate["top_n"] = args.top_n

    teams = []
    for (dataset, team), stats in team_stats.items():
        stats = dict(stats)
        stats["hit_rate"] = stats["draws"] / stats["bets"] if stats["bets"] else 0.0
        stats["dataset"] = dataset
        stats["team"] = team
        teams.append(stats)
    teams.sort(key=lambda row: (-row["hit_rate"], -row["bets"], row["team"]))

    payload = {
        "scope": {"start_season": scope.start_season, "end_season": scope.end_season},
        "aggregate": dict(aggregate),
        "datasets": datasets,
        "team_breakdown": teams[:100],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload["aggregate"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
