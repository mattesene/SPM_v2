from spm.data.coverage import validate_catalog_coverage
from spm.data.historical_catalog import build_catalog


def _catalog():
    return build_catalog(["ita1"], ["2425", "2324"])


def test_coverage_reports_missing_files(tmp_path):
    report = validate_catalog_coverage(_catalog(), tmp_path)
    assert report.expected == 2
    assert report.present == 0
    assert len(report.missing) == 2
    assert not report.complete


def test_coverage_reports_complete_catalog(tmp_path):
    for season in ("2425", "2324"):
        path = tmp_path / "ita1" / season / "ita1.csv"
        path.parent.mkdir(parents=True)
        path.write_text("Date,HomeTeam,AwayTeam,FTHG,FTAG,FTR\n")
    report = validate_catalog_coverage(_catalog(), tmp_path)
    assert report.expected == 2
    assert report.present == 2
    assert report.missing == ()
    assert report.complete
