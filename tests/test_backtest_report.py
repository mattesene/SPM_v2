from spm.backtest.report import BacktestReport


def test_report_accuracy():
    report = BacktestReport.from_predictions(
        ["H", "D", "A", "H"], ["H", "A", "A", "H"]
    )
    assert report.samples == 4
    assert report.correct == 3
    assert report.accuracy == 0.75


def test_empty_report():
    report = BacktestReport.from_predictions([], [])
    assert report.samples == 0
    assert report.accuracy == 0.0
