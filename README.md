# SPM_v2

**Statistical Pareggio Model**

SPM_v2 is a Python project for statistical analysis and modelling of football match draw probabilities.

## Current status

The project now includes a transparent baseline model, CSV ingestion, an SPM-specific scoring engine, and leakage-safe chronological backtesting.

## Architecture

```text
CSV / historical results
          |
          v
      Match / Season
          |
          v
   Team statistics + recent form
          |
          v
   Poisson draw probability
          |
          v
      SPM Engine v1
          |
          v
      SPM Score 0-100
          |
          v
       Backtester
          |
          v
 accuracy / precision / recall / F1 / Brier / ROI
```

## Backtesting rules

The backtester processes matches strictly in chronological order. For every target match, only matches with an earlier date are available to the model. This prevents future information from leaking into historical predictions.

The report includes:

- accuracy;
- precision;
- recall;
- F1;
- Brier score;
- empirical draw-rate baseline Brier score;
- a simple flat-stake ROI proxy.

The ROI is deliberately labelled a proxy: bookmaker odds are not yet imported, so it is not a claim of betting profitability. The next milestone is market-odds ingestion and proper value/ROI analysis.

## Development

Requires Python 3.11+.

```bash
pip install -e ".[test]"
pytest
```
