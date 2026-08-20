from datetime import date

from spm.data.football_data_csv import load_football_data_csv


def test_load_football_data_csv(tmp_path):
    path = tmp_path / "E0.csv"
    path.write_text("Date,HomeTeam,AwayTeam,FTHG,FTAG\n01/08/20,Arsenal,Chelsea,2,1\n", encoding="utf-8")
    rows = load_football_data_csv(path, competition="E0", season="2020-21")
    assert rows[0].date == date(2020, 8, 1)
    assert rows[0].home_goals == 2
    assert rows[0].canonical_home_team
