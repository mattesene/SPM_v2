from datetime import date

from spm.data.results import MatchResult, load_match_results_csv


def test_match_result_outcomes():
    assert MatchResult(date(2025, 1, 1), "A", "B", 1, 1).outcome == "D"
    assert MatchResult(date(2025, 1, 1), "A", "B", 2, 1).outcome == "H"
    assert MatchResult(date(2025, 1, 1), "A", "B", 0, 1).outcome == "A"


def test_load_match_results_csv(tmp_path):
    path = tmp_path / "results.csv"
    path.write_text("Date,HomeTeam,AwayTeam,HomeGoals,AwayGoals\n01/01/2025,A,B,1,0\n", encoding="utf-8")
    records = load_match_results_csv(path)
    assert records[0].outcome == "H"
