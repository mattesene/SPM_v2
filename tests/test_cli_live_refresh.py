from datetime import date

from spm.cli import build_parser


def test_cli_exposes_live_refresh_flag():
    parser = build_parser()
    args = parser.parse_args(["--db", "spm.db", "--live", "--oos", "oos.csv", "--html", "live.html"])
    assert args.live is True
    assert args.refresh_live is False


def test_cli_exposes_refresh_live_flag():
    parser = build_parser()
    args = parser.parse_args(["--db", "spm.db", "--refresh-live", "--oos", "oos.csv", "--html", "live.html"])
    assert args.refresh_live is True
    assert date.fromisoformat(args.as_of)
