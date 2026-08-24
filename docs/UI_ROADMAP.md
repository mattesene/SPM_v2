# SPM_v2 UI implementation roadmap

## Phase 1 — Data contract
- Dashboard DTO: bankroll, P&L, drawdown, today's selections.
- Fixture DTO: SPM score, draw probability, draw odds, implied probability, edge, streak.
- Progression DTO: team, level, current stake, exposure, status.

## Phase 2 — Dashboard
- Responsive mobile-first layout.
- Today's ranked selections.
- Active progressions.
- Bankroll and risk summary.

## Phase 3 — Fixture detail
- Team form and streak history.
- SPM component breakdown.
- Market comparison.
- Selection explanation.

## Phase 4 — Backtest / statistics
- Equity curve.
- ROI and yield.
- Drawdown.
- Breakdown by league, season, SPM score and odds band.

## Phase 5 — Operational controls
- Configure bankroll.
- Configure base stake and progression rules.
- Enable/disable leagues.
- Explicit confirmation before recording a bet.

## Rule
The UI must never calculate a second version of the SPM model. It displays values produced by the canonical Python engine and its validated data pipeline.
