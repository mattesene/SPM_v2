import json

from spm.backtest.oos_aggregation import OOSAggregate
from spm.backtest.oos_report import aggregate_to_dict, write_oos_report


def test_write_oos_report(tmp_path):
    summary = OOSAggregate(2, 10, 4, 2, 0.5)
    assert aggregate_to_dict(summary)["hit_rate"] == 0.5
    target = tmp_path / "report.json"
    write_oos_report(summary, target)
    assert json.loads(target.read_text(encoding="utf-8"))["selected"] == 4
