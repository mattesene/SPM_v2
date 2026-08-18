from spm.ingestion.historical_check import run_historical_coverage_check


if __name__ == "__main__":
    result = run_historical_coverage_check()
    print(f"expected_slices={result.expected_slices}")
    print(f"observed_slices={result.observed_slices}")
    print(f"total_matches={result.total_matches}")
    for item in result.missing_slices:
        print(f"missing={item.competition}:{item.season}")
