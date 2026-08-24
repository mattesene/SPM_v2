from types import SimpleNamespace

from spm.backtest.edge_walk_forward import run_edge_walk_forward


def _row(probability, odds, actual_draw):
    return SimpleNamespace(
        probability=probability,
        draw_odds=odds,
        actual_draw=actual_draw,
    )


def test_walk_forward_does_not_use_test_rows_to_choose_threshold():
    # The two thresholds have identical TRAIN performance. The deterministic
    # tie-break must choose the lower threshold without inspecting TEST.
    train = [_row(0.50, 2.0, 1)] * 4
    test = [_row(0.90, 2.0, 0)] * 2
    rows = train + test
    windows = run_edge_walk_forward(
        rows,
        thresholds=(0.0, 0.10),
        train_size=4,
        test_size=2,
    )
    assert len(windows) == 1
    assert windows[0].threshold == 0.0
    assert windows[0].test_start == 4
    assert windows[0].test_end == 6
