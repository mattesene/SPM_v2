"""Command-line interface for SPM_v2."""

import argparse
from datetime import date

from spm.data.csv import CSVMatchImporter
from spm.data.repository import MatchRepository
from spm.statistics.engine import SPMEngine
from spm.live.config import build_fixture_provider
from spm.live.pipeline import acquire_and_normalize
from spm.live.runner import run_live_from_database
from spm.live.safe_provider import safe_fetch
from spm.web import write_dashboard


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SPM_v2 football draw analyser")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("results", nargs="?", help="CSV file containing historical results")
    source.add_argument("--db", metavar="PATH", help="SQLite database containing normalized historical matches")
    parser.add_argument("--fixture", nargs=2, metavar=("HOME", "AWAY"), action="append", help="Fixture to analyse; repeat for multiple fixtures")
    parser.add_argument("--live", action="store_true", help="Build Live report from persisted upcoming fixtures")
    parser.add_argument("--refresh-live", action="store_true", help="Acquire and validate upcoming fixtures before Live report")
    parser.add_argument("--oos", metavar="PATH", help="OOS ranking file used by Live mode")
    parser.add_argument("--as-of", default=date.today().isoformat(), help="Prediction date in YYYY-MM-DD format")
    parser.add_argument("--window", type=int, default=5, help="Recent-form window")
    parser.add_argument("--decay", type=float, default=0.85, help="Recent-form decay")
    parser.add_argument("--html", metavar="PATH", help="Write a standalone HTML dashboard to PATH")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    as_of = date.fromisoformat(args.as_of)

    if args.live or args.refresh_live:
        if not args.db or not args.oos or not args.html:
            raise SystemExit("Live richiede --db, --oos e --html")
        if args.refresh_live:
            provider = build_fixture_provider()
            fetched = safe_fetch(provider, as_of)
            if not fetched.source_ok:
                raise SystemExit(f"Live acquisition failed: {fetched.error}")
            from spm.data.repository import MatchRepository
            result = acquire_and_normalize(provider, MatchRepository(args.db), from_date=as_of)
            print(f"live_refresh,fetched={result.fetched},written={result.written},rejected={result.rejected},duplicates={result.duplicates_removed}")
        from spm.backtest.oos_ranking import load_oos_ranking
        entries = load_oos_ranking(args.oos)
        run_live_from_database(args.db, entries, as_of=as_of, output=args.html, oos_path=args.oos)
        print(f"live_report,{args.html}")
        return 0

    if not args.fixture:
        raise SystemExit("specificare almeno una --fixture oppure usare --live")
    matches = MatchRepository(args.db).load_matches() if args.db else CSVMatchImporter().load(args.results)
    ranked = SPMEngine(form_window=args.window, decay=args.decay).rank(matches, args.fixture, as_of)[:5]
    print("rank,home,away,draw_probability,spm_score")
    for rank, result in enumerate(ranked, start=1):
        print(f"{rank},{result.home_team},{result.away_team},{result.draw_probability:.4f},{result.spm_score:.2f}")
    if args.html:
        write_dashboard(ranked, as_of=args.as_of, path=args.html)
        print(f"html_report,{args.html}")
    return 0
