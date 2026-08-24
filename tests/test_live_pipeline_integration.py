from datetime import date

from spm.data.fixtures import Fixture
from spm.data.models import Match
from spm.live.data_quality import assess_live_data
from spm.live.selection_adapter import to_live_selections
from spm.live.selection_history import append_selections, load_selections
from spm.live.top5 import score_upcoming_fixtures


def test_live_pipeline_score_adapter_history_is_idempotent(tmp_path):
    as_of = date(2026, 8, 24)
    matches = [
        Match(date(2026, 8, 20), "A", "B", 1, 1),
        Match(date(2026, 8, 21), "A", "C", 2, 0),
    ]
    fixtures = [Fixture("A", "B", date(2026, 8, 25))]

    quality = assess_live_data(matches, fixtures, as_of=as_of)
    assert quality.ok

    scores = score_upcoming_fixtures(matches, fixtures, as_of=as_of)
    selections = to_live_selections(scores, fixtures, as_of=as_of, limit=5)
    assert selections

    history = tmp_path / "history.csv"
    append_selections(history, selections)
    append_selections(history, selections)
    assert load_selections(history) == selections
