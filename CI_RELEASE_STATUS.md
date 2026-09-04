# SPM_v2 release CI status

## Release branch

`main`

The previous release-consolidation PR was merged into `main`; subsequent development is being applied directly to the consolidated main history.

## Required checks

- `pytest -q`
- historical dataset completeness validation
- report regression
- odds/staking regression
- historical backtest completeness gate
- team-progression calibration regression

## Current GitHub Actions observation

The repository workflow files are present, but the GitHub connector currently reports no workflow runs associated with the latest commits. This is treated as a CI infrastructure/visibility issue, not as evidence that the tests passed.

## Latest development

The team-progression calibration report now includes Wilson 95% confidence intervals for observed draw rates and an absolute calibration gap, both overall and per calibration bucket. Regression coverage was added for these diagnostics.

## Release rule

SPM_v2 must not be declared release-ready until the complete test suite has been executed successfully on `main`.
