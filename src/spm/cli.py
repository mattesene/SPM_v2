"""Command-line interface for SPM_v2."""

import argparse
from datetime import date

from spm.data.csv import CSVMatchImporter
from spm.statistics.engine import SPMEngine


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SPM_v2 football draw analyser")
    parser.add_argument("results", help="CSV file containing historical results")
    parser.add_argument("--fixture", nargs=2, metavar=("HOME", "AWAY"), action="append", required=True, help="Fixture to analyse; repeat for multiple fixtures")
    parser.add_argument("--as-of", default=date.today().isoformat(), help="Prediction date in YYYY-MM-DD format")
    parser.add_argument("--window", type=int, default=5, help="Recent-form window")
    parser.add_argument("--decay", type=float, default=0.85, help="Recent-form decay")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    matches = CSVMatchImporter().load(args.results)
    as_of = date.fromisoformat(args.as_of)
    ranked = SPMEngine(form_window=args.window, decay=args.decay).rank(
        matches, [(home, away) for home, away in args.fixture], as_of
    )
    print("rank,home,away,draw_probability,spm_score")
    for rank, result in enumerate(ranked, start=1):
        print(f"{rank},{result.home_team},{result.away_team},{result.draw_probability:.4f},{result.spm_score:.2f}")
    return 0
