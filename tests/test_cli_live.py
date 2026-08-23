from datetime import date

from spm.backtest.oos_ranking import OOSRankingEntry
from spm.data.fixtures import Fixture
from spm.data.models import Match
from spm.data.repository import MatchRepository
from spm.cli import main


def test_cli_live_generates_report(tmp_path, monkeypatch) -> None:
    db = tmp_path / "spm.db"
    repo = MatchRepository(db)
    repo.upsert_match(Match("H0", "A0", date(2026, 8, 1), 1, 1))
    repo.upsert_match(Match("H1", "A1", date(2026, 8, 2), 0, 0))
    repo.upsert_fixture(Fixture("H0", "A0", date(2026, 8, 24)))
    repo.upsert_fixture(Fixture("H1", "A1", date(2026, 8, 25)))
    oos = tmp_path / "oos.csv"
    oos.write_text(
        "fixture,bets,roi,draw_rate,profitable_window_rate,mean_stake,max_drawdown,windows\n"
        "H0 vs A0,20,100,.10,.80,0,0,0\n"
        "H1 vs A1,20,90,.10,.80,0,0,0\n",
        encoding="utf-8",
    )
    html = tmp_path / "live.html"
    monkeypatch.setattr("sys.argv", ["spm", "--db", str(db), "--live", "--oos", str(oos), "--html", str(html), "--as-of", "2026-08-23"])
    assert main() == 0
    assert html.exists()
    assert "SPM_v2 · Live" in html.read_text(encoding="utf-8")
