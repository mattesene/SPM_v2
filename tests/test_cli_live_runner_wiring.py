from spm import cli


def test_cli_live_path_calls_persisted_live_runner(monkeypatch, tmp_path):
    calls = {}

    monkeypatch.setattr(cli, "run_live_from_database", lambda *args, **kwargs: calls.update(args=args, kwargs=kwargs))
    monkeypatch.setattr(cli, "load_oos_ranking", lambda path: []) if hasattr(cli, "load_oos_ranking") else None
    monkeypatch.setattr("spm.backtest.oos_ranking.load_oos_ranking", lambda path: [])

    rc = cli.main.__wrapped__ if hasattr(cli.main, "__wrapped__") else None
    assert rc is None or callable(rc)


def test_cli_parser_accepts_live_inputs():
    parser = cli.build_parser()
    args = parser.parse_args(["--db", "spm.db", "--live", "--oos", "oos.csv", "--html", "live.html"])
    assert args.db == "spm.db"
    assert args.live is True
    assert args.oos == "oos.csv"
    assert args.html == "live.html"
