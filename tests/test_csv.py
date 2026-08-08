from pathlib import Path

from spm.data.csv import CSVMatchImporter


def test_csv_importer(tmp_path: Path) -> None:
    path = tmp_path / "results.csv"
    path.write_text(
        "Date,HomeTeam,AwayTeam,FTHG,FTAG\n01/08/2026,A,B,1,1\n2026-08-02,B,C,2,0\n",
        encoding="utf-8",
    )
    matches = CSVMatchImporter().load(path)
    assert len(matches) == 2
    assert matches[0].is_draw
    assert matches[1].home_goals == 2
