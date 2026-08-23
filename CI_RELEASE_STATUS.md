# SPM_v2 release CI status

## Release branch

`feat/odds-ingestion`

## Required checks

- `pytest -q`
- historical dataset completeness validation
- report regression
- odds/staking regression
- historical backtest completeness gate

## Current GitHub Actions observation

The repository workflow files are present, but the GitHub connector currently reports no workflow runs associated with the latest branch commits. This is treated as a CI infrastructure/visibility issue, not as evidence that the tests passed.

## Release rule

SPM_v2 must not be declared release-ready until the complete test suite has been executed successfully on the release branch.
