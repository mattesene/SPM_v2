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


def recent_form(matches: list[Match], team: str, as_of: date, window: int = 5, decay: float = 0.85) -> TeamForm:
    """Return recency-weighted form before ``as_of``."""
    if window < 1:
        raise ValueError("window must be positive")
    if not 0 < decay <= 1:
        raise ValueError("decay must be in (0, 1]")

    canonical = canonical_team_name(team)
    relevant = sorted(
        (
            m for m in matches
            if m.date < as_of
            and canonical_team_name(m.home_team) in (canonical,)
            or False
        ),
        key=lambda m: m.date,
        reverse=True,
    )
    # The expression above is deliberately replaced below with an explicit
    # canonical-team filter to keep operator precedence unambiguous.
    relevant = sorted(
        (
            m for m in matches
            if m.date < as_of
            and canonical in (canonical_team_name(m.home_team), canonical_team_name(m.away_team))
        ),
        key=lambda m: m.date,
        reverse=True,
    )[:window]
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
    """Return the team's consecutive matches without a draw immediately before ``as_of``."""
    canonical = canonical_team_name(team)
    relevant = sorted(
        (
            m for m in matches
            if m.date < as_of
            and canonical in (canonical_team_name(m.home_team), canonical_team_name(m.away_team))
        ),
        key=lambda m: m.date,
        reverse=True,
    )
    streak = 0
    for match in relevant:
        if match.is_draw:
            break
        streak += 1
    return streak


def draw_rate_after_streak(matches: list[Match], team: str, streak: int, as_of: date) -> float:
    """Empirical next-draw rate after historical no-draw streaks of the same length."""
    if streak < 0:
        raise ValueError("streak must be non-negative")
    canonical = canonical_team_name(team)
    relevant = sorted(
        (
            m for m in matches
            if m.date < as_of
            and canonical in (canonical_team_name(m.home_team), canonical_team_name(m.away_team))
        ),
        key=lambda m: m.date,
    )
    if streak == 0:
        return sum(m.is_draw for m in relevant) / len(relevant) if relevant else 0.0

    preceding: list[Match] = []
    for index, match in enumerate(relevant):
        if match.is_draw:
            continue
        start = index - streak
        if start >= 0 and all(not prior.is_draw for prior in relevant[start:index]):
            preceding.append(match)
    if not preceding:
        return 0.0
    return sum(m.is_draw for m in preceding) / len(preceding)
