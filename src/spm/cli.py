"""Command-line interface for SPM_v2."""

import argparse
from datetime import date

from spm.data.csv import CSVMatchImporter
from spm.data.repository import MatchRepository
from spm.statistics.engine import SPMEngine
from spm.web import write_dashboard


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SPM_v2 football draw analyser")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("results", nargs="?", help="CSV file containing historical results")
    source.add_argument("--db", metavar="PATH", help="SQLite database containing normalized historical matches")
    parser.add_argument("--fixture", nargs=2, metavar=("HOME", "AWAY"), action="append", required=True, help="Fixture to analyse; repeat for multiple fixtures")
    parser.add_argument("--as-of", default=date.today().isoformat(), help="Prediction date in YYYY-MM-DD format")
    parser.add_argument("--window", type=int, default=5, help="Recent-form window")
    parser.add_argument("--decay", type=float, default=0.85, help="Recent-form decay")
    parser.add_argument("--html", metavar="PATH", help="Write a standalone HTML dashboard to PATH")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    matches = MatchRepository(args.db).load_matches() if args.db else CSVMatchImporter().load(args.results)
    as_of = date.fromisoformat(args.as_of)
    ranked = SPMEngine(form_window=args.window, decay=args.decay).rank(
        matches, [(home, away) for home, away in args.fixture], as_of
    )
    print("rank,home,away,draw_probability,spm_score")
    for rank, result in enumerate(ranked, start=1):
        print(f"{rank},{result.home_team},{result.away_team},{result.draw_probability:.4f},{result.spm_score:.2f}")
    if args.html:
        write_dashboard(ranked, as_of=args.as_of, path=args.html)
        print(f"html_report,{args.html}")
    return 0
