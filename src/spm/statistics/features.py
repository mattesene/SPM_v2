"""Feature engineering for draw probability modelling."""

from dataclasses import dataclass
from datetime import date
from math import exp

from spm.data.models import Match
from spm.data.normalization import canonical_team_name


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


def _team_matches(matches: list[Match], team: str, as_of: date) -> list[Match]:
    canonical = canonical_team_name(team)
    return sorted(
        (
            m for m in matches
            if m.date < as_of
            and canonical in (canonical_team_name(m.home_team), canonical_team_name(m.away_team))
        ),
        key=lambda m: m.date,
        reverse=True,
    )


def recent_form(matches: list[Match], team: str, as_of: date, window: int = 5, decay: float = 0.85) -> TeamForm:
    """Return recency-weighted form before ``as_of``."""
    if window < 1:
        raise ValueError("window must be positive")
    if not 0 < decay <= 1:
        raise ValueError("decay must be in (0, 1]")

    canonical = canonical_team_name(team)
    relevant = _team_matches(matches, canonical, as_of)[:window]
    total_weight = 0.0
    points = goals_for = goals_against = draws = 0.0

    for index, match in enumerate(relevant):
        weight = exp(index * __import__('math').log(decay))
        if canonical_team_name(match.home_team) == canonical:
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


def draw_streak(matches: list[Match], team: str, as_of: date) -> int:
    """Return consecutive matches without a draw immediately before ``as_of``."""
    streak = 0
    for match in _team_matches(matches, team, as_of):
        if match.is_draw:
            break
        streak += 1
    return streak


def draw_rate_after_streak(
    matches: list[Match],
    team: str,
    streak: int,
    as_of: date,
    *,
    prior_strength: float = 5.0,
) -> float:
    """Estimate draw probability after an identical no-draw streak.

    The historical conditional rate is shrunk toward the team's overall draw
    rate when only a few matching streaks are available. This prevents a
    single historical occurrence from producing an unjustified 100% signal.
    """
    if streak < 0:
        raise ValueError("streak must be non-negative")
    if prior_strength < 0:
        raise ValueError("prior_strength must be non-negative")

    relevant = list(reversed(_team_matches(matches, team, as_of)))
    if not relevant:
        return 0.0
    overall_rate = sum(m.is_draw for m in relevant) / len(relevant)
    if streak == 0:
        return overall_rate

    opportunities = draws = 0
    for index, match in enumerate(relevant):
        if not match.is_draw or index < streak:
            continue
        previous = relevant[index - streak:index]
        if len(previous) == streak and all(not m.is_draw for m in previous):
            opportunities += 1
            draws += 1

    if not opportunities:
        return overall_rate
    if prior_strength == 0:
        return draws / opportunities
    return (draws + prior_strength * overall_rate) / (opportunities + prior_strength)
