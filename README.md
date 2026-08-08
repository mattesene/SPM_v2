# SPM_v2

**Statistical Pareggio Model**

SPM_v2 is a Python project for statistical analysis and modelling of football match draw probabilities.

## Current status

The project is in initial development. The first milestone establishes the domain model and probability layer that will support the SPM engine.

## Structure

```text
src/spm/
├── data/          # Domain models and data ingestion
└── statistics/    # Statistical estimators and probability functions
tests/             # Automated tests
```

## Development

Requires Python 3.11+.

```bash
pip install -e ".[test]"
pytest
```

The model is intentionally being built in small, testable components so that data sources, statistical assumptions, and prediction logic remain independently replaceable.
