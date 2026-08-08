"""SPM prediction engine."""

from dataclasses import dataclass
from datetime import date

from spm.data.models import Match
from spm.data.season import Season
from spm.statistics.features import recent_form
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


class SPMEngine:
    """Rank fixtures using calibrated, interpretable draw signals."""

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
        probability = min(1.0, max(0.0, sum(x * w for x, w in zip(features, self.weights))))
        return SPMScore(
            home_team, away_team, probability, probability * 100.0,
            form_balance, draw_signal, goal_balance_signal, self.weights,
        )

    def rank(self, matches: list[Match], fixtures: list[tuple[str, str]], as_of: date) -> list[SPMScore]:
        return sorted(
            (self.score(matches, home, away, as_of) for home, away in fixtures),
            key=lambda item: item.spm_score,
            reverse=True,
        )
