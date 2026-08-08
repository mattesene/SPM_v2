"""First Statistical Pareggio Model (SPM) estimator."""

from dataclasses import dataclass

from spm.data.season import Season


@dataclass(frozen=True, slots=True)
class DrawPrediction:
    home_team: str
    away_team: str
    probability: float
    expected_home_goals: float
    expected_away_goals: float


class PareggioModel:
    """Estimate draw probability from empirical scoring rates.

    This is deliberately a transparent baseline. It combines the expected
    scoring rates of each team and converts them into a draw probability by
    summing the independent Poisson probabilities for equal scores.
    """

    def __init__(self, max_goals: int = 10) -> None:
        if max_goals < 1:
            raise ValueError("max_goals must be positive")
        self.max_goals = max_goals

    def predict(self, season: Season, home_team: str, away_team: str) -> DrawPrediction:
        home = season.team_stats(home_team)
        away = season.team_stats(away_team)
        if home.matches == 0 or away.matches == 0:
            raise ValueError("Both teams need at least one historical match")

        # Baseline expected goals: each team's scoring average blended with
        # the opponent's conceded average. Home advantage is intentionally
        # not hard-coded until it is estimated from the dataset.
        lambda_home = (home.goals_for_avg + away.goals_against_avg) / 2
        lambda_away = (away.goals_for_avg + home.goals_against_avg) / 2

        probability = sum(
            _poisson(k, lambda_home) * _poisson(k, lambda_away)
            for k in range(self.max_goals + 1)
        )
        return DrawPrediction(
            home_team, away_team, probability, lambda_home, lambda_away
        )


def _poisson(k: int, lam: float) -> float:
    if lam == 0:
        return 1.0 if k == 0 else 0.0
    probability = 1.0
    for i in range(1, k + 1):
        probability *= lam / i
    import math
    return math.exp(-lam) * probability
