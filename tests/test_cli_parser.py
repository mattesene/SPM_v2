from spm.cli import build_parser


def test_parser_accepts_sqlite_source() -> None:
    args = build_parser().parse_args(["--db", "spm.db", "--fixture", "Inter", "Milan"])
    assert args.db == "spm.db"
    assert args.results is None


def test_parser_accepts_csv_source() -> None:
    args = build_parser().parse_args(["results.csv", "--fixture", "Inter", "Milan"])
    assert args.results == "results.csv"
    assert args.db is None
