# SPM_v2

**Statistical Pareggio Model**

SPM_v2 is a Python application for statistical analysis and modelling of football match draw probabilities.

## Current status

SPM_v2 provides:

- validated football-result domain models;
- CSV historical-data ingestion;
- deterministic team-name normalization;
- multi-source match reconciliation;
- SQLite persistence with source provenance;
- recency-weighted form features;
- Poisson draw-probability baseline;
- configurable SPM feature weights;
- SPM Score from 0 to 100;
- fixture ranking;
- chronological backtesting without future-data leakage;
- deterministic weight calibration;
- walk-forward out-of-sample validation;
- historical draw-market odds ingestion and deterministic match/odds reconciliation;
- odds-aware staking simulation for the draw progression strategy;
- aggregate historical backtest reporting by competition/season;
- automated historical-data validation in GitHub Actions;
- automated tests through GitHub Actions;
- command-line prediction interface.

## Data-source strategy

The supplied sources are intentionally assigned different roles rather than blindly merging them. Diretta.it, Sofascore and FBref are registered as independent results/fixture references; Sofascore and FBref also cover rich team/match/player statistics; WhoScored is reserved for advanced statistical cross-checks; CIES Football Observatory is treated as contextual/research data.

The ingestion layer records source provenance so the same match or statistic can be reconciled across providers. Automated collection will only use access methods permitted by each provider's terms and technical restrictions; a website being listed as a source does not imply permission to bypass anti-bot controls or access restrictions.

Historical market prices are treated separately from match results. A draw price is joined deterministically to the corresponding canonical fixture and is used only after the chronological model decision, preventing future market information from leaking into the model features.

## Data pipeline

```text
Provider adapters
      |
      v
Canonical MatchRecord + historical market odds
      |
      v
Team-name normalization / deterministic reconciliation
      |
      v
SQLite + provenance
      |
      v
SPM statistics / model
      |
      v
Poisson baseline + SPM feature vector
      |
      v
Calibrated weights
      |
      v
Chronological OOS probability / selection
      |
      +--> historical draw odds
      |
      v
Odds-aware staking simulation
      |
      v
Ranking + backtesting + walk-forward validation
```

## Historical validation

The default historical catalog contains 35 datasets covering the configured 2019/20–2025/26 scope. GitHub Actions validates that every expected dataset can be downloaded or retrieved from cache before the historical backtest is executed. The validation and backtest reports are uploaded as CI artifacts.

The historical backtest processes matches chronologically and keeps target-match information out of the prediction. Market odds are used for staking/evaluation after the model selection, not as a feature of the same prediction.

## CLI

Install the package:

```bash
pip install -e ".[test]"
```

Analyse one or more fixtures:

```bash
spm results.csv --fixture "Inter" "Milan" --fixture "Roma" "Lazio" --as-of 2026-08-08
```

The CSV importer expects these columns by default:

`Date, HomeTeam, AwayTeam, FTHG, FTAG`

Supported dates are `DD/MM/YYYY`, `DD/MM/YY` and `YYYY-MM-DD`.

## Validation

The backtester and walk-forward validator process matches chronologically. A target match never contributes information to its own prediction or to an earlier prediction. Calibration weights are estimated only on the training window and evaluated on later observations.

The evaluation layer reports accuracy, precision, recall, F1 and Brier score. Odds-aware staking uses the historical draw price actually associated with the selected fixture and does not substitute an assumed constant market price.

## Development

Requires Python 3.11+.

```bash
pytest
python -m spm --help
```

The project intentionally keeps the core model dependency-light so statistical assumptions and validation remain transparent and reproducible.
