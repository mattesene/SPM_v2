from spm.data.catalog_report import default_coverage_report, format_coverage_report


def test_default_report_uses_five_competitions_and_seven_seasons(tmp_path):
    report = default_coverage_report(tmp_path)
    assert report.expected == 35
    assert report.present == 0
    assert len(report.missing) == 35
    text = format_coverage_report(report)
    assert "expected=35" in text
    assert "complete=False" in text
