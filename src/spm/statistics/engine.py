"""SPM prediction engine."""

from dataclasses import dataclass
from datetime import date

from spm.data.models import Match
from spm.data.season import Season
from spm.statistics.features import draw_rate_after_streak, draw_streak, recent_form
from spm.statistics.model import PareggioModel


DEFAULT_WEIGHTS = (0.60, 0.15, 0.15, 0.10)


@dataclass(frozen=True, slots=True)
class SPMScore:
    home_team: str
    away_team: str
    draw_probability: float
    spm_score: float
    form_balance: float
    draw_signal: float
    goal_balance_signal: float
    weights: tuple[float, float, float, float]
    selected_team: str = ""
    selected_team_draw_rate: float = 0.0
    selected_team_streak: int = 0
    selected_team_streak_draw_rate: float = 0.0
    team_probability: float = 0.0


class SPMEngine:
    """Rank upcoming fixtures by the strength of the team-level draw signal."""

    def __init__(self, form_window: int = 5, decay: float = 0.85, weights: tuple[float, float, float, float] = DEFAULT_WEIGHTS) -> None:
        if form_window < 1:
            raise ValueError("form_window must be positive")
        if not 0 < decay <= 1:
            raise ValueError("decay must be in (0, 1]")
        if len(weights) != 4 or any(w < 0 for w in weights) or abs(sum(weights) - 1.0) > 1e-9:
            raise ValueError("weights must contain four non-negative values summing to 1")
        self.form_window = form_window
        self.decay = decay
        self.weights = weights
        self.model = PareggioModel()

    def score(self, matches: list[Match], home_team: str, away_team: str, as_of: date) -> SPMScore:
        historical = [m for m in matches if m.date < as_of]
        prediction = self.model.predict(Season(historical), home_team, away_team)
        home_form = recent_form(historical, home_team, as_of, self.form_window, self.decay)
        away_form = recent_form(historical, away_team, as_of, self.form_window, self.decay)

        form_balance = max(0.0, 1.0 - abs(home_form.points_per_match - away_form.points_per_match) / 3.0)
        draw_signal = 1.0 - abs(home_form.draw_rate - away_form.draw_rate)
        goal_gap = abs(home_form.goal_balance - away_form.goal_balance)
        goal_balance_signal = max(0.0, 1.0 - min(goal_gap / 3.0, 1.0))

        features = (prediction.probability, form_balance, draw_signal, goal_balance_signal)
        match_probability = min(1.0, max(0.0, sum(x * w for x, w in zip(features, self.weights))))

        team_rows = []
        for team, form in ((home_team, home_form), (away_team, away_form)):
            streak = draw_streak(historical, team, as_of)
            streak_rate = draw_rate_after_streak(historical, team, streak, as_of)
            # Team propensity is driven primarily by observed draw frequency,
            # with the streak-conditioned rate receiving extra weight when data exists.
            team_rate = form.draw_rate
            propensity = team_rate * 0.55 + streak_rate * 0.45 if streak_rate > 0 else team_rate
            team_probability = min(1.0, max(0.0, 0.70 * match_probability + 0.30 * propensity))
            team_rows.append((team, team_probability, team_rate, streak, streak_rate))

        selected_team, team_probability, team_rate, streak, streak_rate = max(
            team_rows,
            key=lambda row: (row[1], row[3], row[2], row[0]),
        )
        return SPMScore(
            home_team, away_team, team_probability, team_probability * 100.0,
            form_balance, draw_signal, goal_balance_signal, self.weights,
            selected_team, team_rate, streak, streak_rate, team_probability,
        )

    def rank(self, matches: list[Match], fixtures: list[tuple[str, str]], as_of: date) -> list[SPMScore]:
        return sorted(
            (self.score(matches, home, away, as_of) for home, away in fixtures),
            key=lambda item: (-item.team_probability, -item.selected_team_streak, item.selected_team),
        )
