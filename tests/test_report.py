from pathlib import Path

from spm.statistics.report import aggregate_directory, csv_rows


def test_aggregate_directory(tmp_path: Path) -> None:
    (tmp_path / "a.csv").write_text(
        "Date,HomeTeam,AwayTeam,FTHG,FTAG\n"
        "01/07/2026,A,B,1,1\n"
        "02/07/2026,A,C,2,0\n"
        "03/07/2026,B,C,0,0\n"
        "04/07/2026,A,B,1,1\n",
        encoding="utf-8",
    )
    report = aggregate_directory(tmp_path)
    assert len(report.datasets) == 1
    assert report.evaluated == 1
    assert report.skipped == 3
    assert 0 <= report.brier_score <= 1
    assert 0 <= report.actual_draw_rate <= 1
    assert csv_rows(report)[0].startswith("dataset,")
