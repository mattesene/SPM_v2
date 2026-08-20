from spm.data.catalog_report import default_coverage_report, format_coverage_report


def test_default_report_uses_five_competitions_and_six_seasons(tmp_path):
    report = default_coverage_report(tmp_path)
    assert report.expected == 30
    assert report.present == 0
    assert len(report.missing) == 30
    text = format_coverage_report(report)
    assert "expected=30" in text
    assert "complete=False" in text
