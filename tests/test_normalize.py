import pytest

from spm.data.normalize import normalize_team_name, same_team


def test_normalize_team_name_is_stable() -> None:
    assert normalize_team_name("  Paris Saint-Germain  ") == "paris saint germain"
    assert normalize_team_name("Bayern München") == "bayern munchen"
    assert normalize_team_name("FC  Köln") == "fc koln"


def test_same_team() -> None:
    assert same_team("Bayern München", "bayern munchen")
    assert not same_team("Milan", "Inter")


def test_normalize_requires_string() -> None:
    with pytest.raises(TypeError):
        normalize_team_name(123)  # type: ignore[arg-type]
