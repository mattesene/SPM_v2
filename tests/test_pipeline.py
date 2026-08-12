from datetime import date

from spm.data.pipeline import ingest_football_data_csv
from spm.data.repository import MatchRepository


def test_football_data_pipeline(tmp_path):
    csv_path = tmp_path / "ITA.csv"
    csv_path.write_text(
        "Date,HomeTeam,AwayTeam,FTHG,FTAG\n"
        "01/08/26,Team A,Team B,1,0\n"
        "02/08/26,Team C,Team D,2,2\n",
        encoding="utf-8",
    )
    repository = MatchRepository(tmp_path / "spm.db")
    report = ingest_football_data_csv(
        csv_path, repository, competition="Serie A", season="2026/27", as_of=date(2026, 8, 3)
    )
    assert report.received == 2
    assert report.rejected == 0
    assert report.stored == 2
    assert report.completed == 2
    assert repository.count() == 2
