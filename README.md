# SPM_v2

**Statistical Pareggio Model**

SPM_v2 is a Python project for statistical analysis and modelling of football match draw probabilities.

## Current status

The project is in initial development. The current milestone provides the first end-to-end statistical baseline: match domain data, season/team aggregation, and an interpretable draw-probability estimator based on Poisson scoring rates.

## Structure

```text
src/spm/
├── data/
│   ├── models.py    # Match domain model
│   └── season.py    # Season and team statistics
└── statistics/
    ├── probability.py # Probability utilities
    └── model.py       # Baseline draw model
tests/                 # Automated tests
```

## Development

Requires Python 3.11+.

```bash
pip install -e ".[test]"
pytest
```

The model is intentionally built in small, testable components so that data sources, statistical assumptions, and prediction logic remain independently replaceable.

## Baseline model

For a fixture `home_team` vs `away_team`, the baseline estimates expected goals as the mean of:

- the home team's historical goals scored and the away team's goals conceded;
- the away team's historical goals scored and the home team's goals conceded.

The draw probability is then the sum of the probabilities of equal scores (0-0, 1-1, 2-2, ...) under independent Poisson scoring distributions.

This is a transparent baseline, not the final SPM methodology. The next milestone will add real data ingestion, home/away-specific statistics, recency weighting, model calibration and backtesting.
