from spm.backtest.competition_runner import run_by_competition
from spm.ingestion.historical import COMPETITIONS
from spm.ingestion.historical_batch import load_historical_batch
from spm.ingestion.seasons import season_codes


if __name__ == "__main__":
    records = load_historical_batch(COMPETITIONS, season_codes())
    results = run_by_competition(records, min_history=3)
    total = sum(len(items) for items in results.values())
    selected = sum(sum(item.selected for item in items) for items in results.values())
    print(f"competitions={len(results)}")
    print(f"backtest_observations={total}")
    print(f"selected={selected}")
    for competition, items in results.items():
        print(f"{competition}: observations={len(items)} selected={sum(item.selected for item in items)}")
