from spm.cli import build_parser


def test_cli_requires_fixture() -> None:
    parser = build_parser()
    args = parser.parse_args(["results.csv", "--fixture", "A", "B"])
    assert args.fixture == [["A", "B"]]
    assert args.as_of


def test_cli_accepts_multiple_fixtures_and_html() -> None:
    parser = build_parser()
    args = parser.parse_args([
        "results.csv",
        "--fixture", "A", "B",
        "--fixture", "C", "D",
        "--html", "reports/spm.html",
    ])
    assert args.fixture == [["A", "B"], ["C", "D"]]
    assert args.html == "reports/spm.html"
