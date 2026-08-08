"""SPM Engine v1: combine transparent statistical signals into an X score."""

from dataclasses import dataclass
from datetime import date

from spm.data.models import Match
from spm.statistics.features import recent_form
from spm.statistics.model import PareggioModel


@dataclass(frozen=True, slots=True)
class SPMScore:
    home_team: str
    away_team: str
    draw_probability: float
    spm_score: float
    form_balance: float
    draw_signal: float
    goal_balance_signal: float


class SPMEngine:
    """Rank a fixture using model probability plus draw-specific signals."""

    def __init__(self, form_window: int = 5, decay: float = 0.85) -> None:
        self.form_window = form_window
        self.decay = decay
        self.model = PareggioModel()

    def score(self, matches: list[Match], home_team: str, away_team: str, as_of: date) -> SPMScore:
        historical = [m for m in matches if m.date < as_of]
        prediction = self.model.predict(__import__('spm.data.season', fromlist=['Season']).Season(historical), home_team, away_team)
        home_form = recent_form(historical, home_team, as_of, self.form_window, self.decay)
        away_form = recent_form(historical, away_team, as_of, self.form_window, self.decay)

        # 1 means balanced form; 0 means a large form gap.
        form_gap = abs(home_form.points_per_match - away_form.points_per_match)
        form_balance = max(0.0, 1.0 - form_gap / 3.0)

        # Draw history is stronger when both teams have similar draw rates.
        draw_signal = 1.0 - abs(home_form.draw_rate - away_form.draw_rate)

        # Low absolute goal-balance difference is a positive draw signal.
        goal_gap = abs(home_form.goal_balance - away_form.goal_balance)
        goal_balance_signal = max(0.0, 1.0 - min(goal_gap / 3.0, 1.0))

        score = 100.0 * (
            0.60 * prediction.probability
            + 0.15 * form_balance
            + 0.15 * draw_signal
            + 0.10 * goal_balance_signal
        )
        return SPMScore(home_team, away_team, prediction.probability, score, form_balance, draw_signal, goal_balance_signal)

    def rank(self, matches: list[Match], fixtures: list[tuple[str, str]], as_of: date) -> list[SPMScore]:
        scores = [self.score(matches, home, away, as_of) for home, away in fixtures]
        return sorted(scores, key=lambda item: item.spm_score, reverse=True)
