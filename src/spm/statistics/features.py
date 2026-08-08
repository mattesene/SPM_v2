"""Feature engineering for draw probability modelling."""

from dataclasses import dataclass
from datetime import date
from math import exp

from spm.data.models import Match


@dataclass(frozen=True, slots=True)
class TeamForm:
    matches: int
    points: float
    goals_for: float
    goals_against: float
    draws: float

    @property
    def points_per_match(self) -> float:
        return self.points / self.matches if self.matches else 0.0

    @property
    def goal_balance(self) -> float:
        return (self.goals_for - self.goals_against) / self.matches if self.matches else 0.0

    @property
    def draw_rate(self) -> float:
        return self.draws / self.matches if self.matches else 0.0


def recent_form(matches: list[Match], team: str, as_of: date, window: int = 5, decay: float = 0.85) -> TeamForm:
    """Return recency-weighted form before ``as_of``.

    Matches are sorted newest-first. The newest match has weight 1 and each
    older match is multiplied by ``decay``.
    """
    if window < 1:
        raise ValueError("window must be positive")
    if not 0 < decay <= 1:
        raise ValueError("decay must be in (0, 1]")

    relevant = sorted((m for m in matches if m.date < as_of and team in (m.home_team, m.away_team)), key=lambda m: m.date, reverse=True)[:window]
    total_weight = 0.0
    points = goals_for = goals_against = draws = 0.0

    for index, match in enumerate(relevant):
        weight = exp(index * __import__('math').log(decay))
        if match.home_team == team:
            gf, ga = match.home_goals, match.away_goals
        else:
            gf, ga = match.away_goals, match.home_goals
        points_value = 3 if gf > ga else 1 if gf == ga else 0
        total_weight += weight
        points += points_value * weight
        goals_for += gf * weight
        goals_against += ga * weight
        draws += (gf == ga) * weight

    if not total_weight:
        return TeamForm(0, 0.0, 0.0, 0.0, 0.0)
    return TeamForm(
        len(relevant), points / total_weight, goals_for / total_weight,
        goals_against / total_weight, draws / total_weight,
    )
