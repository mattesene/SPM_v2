from spm.backtest.oos_ranking import OOSRankingEntry
from spm.backtest.top5 import select_top5


def entry(key, score, bets=20, rate=.6):
    return OOSRankingEntry(key, 3, bets, score * 1000, score, 0, rate, score)


def test_top5_applies_reliability_filters_and_limits_size():
    rows = [entry(chr(65 + i), 1.0 - i / 10) for i in range(7)]
    rows.append(entry("X", 2.0, bets=10, rate=.9))
    result = select_top5(rows)
    assert result.eligible == 7
    assert len(result.entries) == 5
    assert result.entries[0].key == "A"


def test_top5_rejects_unreliable_rows():
    result = select_top5([entry("A", 1, bets=10), entry("B", 2, rate=.4)])
    assert result.entries == ()
