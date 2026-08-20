from datetime import date

from spm.data.football_data_csv import load_football_data_odds


def test_load_draw_odds_prefers_avgd(tmp_path):
    path = tmp_path / "E0.csv"
    path.write_text("Date,HomeTeam,AwayTeam,FTHG,FTAG,AvgD,MaxD,B365D\n01/08/20,Arsenal,Chelsea,2,1,3.25,3.4,3.1\n", encoding="utf-8")
    odds = load_football_data_odds(path)
    assert odds == () or odds[0].draw_odds == 3.25
