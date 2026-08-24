from spm.cli import build_parser


def test_cli_requires_fixture() -> None:
    parser = build_parser()
    args = parser.parse_args(["results.csv", "--fixture", "A", "B"])
    assert args.fixture == [["A", "B"]]
    assert args.as_of
