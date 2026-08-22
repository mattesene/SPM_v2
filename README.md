# SPM_v2

**Statistical Pareggio Model**

SPM_v2 is a Python application for statistical analysis and modelling of football match draw probabilities.

## Current status

SPM_v2 now provides:

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
- market odds and odds-aware staking/backtesting;
- out-of-sample edge evaluation and stability-aware Top 5 ranking;
- machine-readable OOS reporting;
- standalone HTML prediction dashboard;
- automated tests through GitHub Actions;
- command-line prediction interface.

## Data-source strategy

The supplied sources are intentionally assigned different roles rather than blindly merging them. Diretta.it, Sofascore and FBref are registered as independent results/fixture references; Sofascore and FBref also cover rich team/match/player statistics; WhoScored is reserved for advanced statistical cross-checks; CIES Football Observatory is treated as contextual/research data.

The ingestion layer records source provenance so the same match or statistic can be reconciled across providers. Automated collection will only use access methods permitted by each provider's terms and technical restrictions; a website being listed as a source does not imply permission to bypass anti-bot controls or access restrictions.

## Data pipeline

```text
Provider adapters
      |
      v
Canonical MatchRecord
      |
      v
Team-name normalization
      |
      v
Multi-source reconciliation
      |
      v
SQLite + provenance
      |
      v
SPM statistics / model
```

The provider layer is intentionally adapter-based. A source can be added without changing the statistical engine. The current implementation includes a canonical CSV adapter and the interfaces needed for permitted provider-specific adapters.

## Architecture

```text
External sources
     |
     v
Source registry + provenance
     |
     v
Canonical MatchRecord
     |
     v
Match / Season
     |
     +--> team statistics
     +--> recent form
     +--> draw history
     +--> goal balance
     |
     v
Poisson baseline
     |
     v
SPM feature vector
     |
     v
Calibrated weights
     |
     v
SPM probability / score
     |
     v
Ranking + backtesting + walk-forward validation
     |
     v
Market edge + staking + OOS stability
     |
     v
HTML dashboard
```

## CLI

Install the package:

```bash
pip install -e ".[test]"
```

Analyse one or more fixtures:

```bash
spm results.csv --fixture "Inter" "Milan" --fixture "Roma" "Lazio" --as-of 2026-08-08
```

Generate a standalone HTML dashboard in addition to the CSV output:

```bash
spm results.csv --fixture "Inter" "Milan" --fixture "Roma" "Lazio" --as-of 2026-08-08 --html reports/spm.html
```

The generated page is self-contained and can be opened directly in a browser; it requires no web server or frontend dependency.

The CSV importer expects these columns by default:

`Date, HomeTeam, AwayTeam, FTHG, FTAG`

Supported dates are `DD/MM/YYYY`, `DD/MM/YY` and `YYYY-MM-DD`.

## Validation

The backtester and walk-forward validator process matches chronologically. A target match never contributes information to its own prediction or to an earlier prediction. Calibration weights are estimated only on the training window and evaluated on later observations.

The evaluation layer reports accuracy, precision, recall, F1 and Brier score. Economic evaluation uses imported historical market odds and keeps price availability and exact match alignment explicit. OOS ranking is restricted to observations with usable prices and includes reliability/stability diagnostics.

## Development

Requires Python 3.11+.

```bash
pytest
python -m spm --help
```

The project intentionally keeps the core model dependency-light so statistical assumptions and validation remain transparent and reproducible.
