"""Domain models used by the SPM data layer."""

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class Match:
    """A played football match and its final score."""

    date: date
    home_team: str
    away_team: str
    home_goals: int
    away_goals: int

    def __post_init__(self) -> None:
        if self.home_goals < 0 or self.away_goals < 0:
            raise ValueError("Goals cannot be negative")
        if not self.home_team.strip() or not self.away_team.strip():
            raise ValueError("Team names cannot be empty")

    @property
    def is_draw(self) -> bool:
        return self.home_goals == self.away_goals

    @property
    def result(self) -> str:
        if self.home_goals > self.away_goals:
            return "H"
        if self.home_goals < self.away_goals:
            return "A"
        return "D"
