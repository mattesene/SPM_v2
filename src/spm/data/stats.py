"""Optional advanced match statistics normalized across providers."""
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MatchStats:
    match_key: tuple
    source: str
    xg_home: float | None = None
    xg_away: float | None = None
    shots_home: int | None = None
    shots_away: int | None = None
    shots_on_target_home: int | None = None
    shots_on_target_away: int | None = None
    possession_home: float | None = None
    possession_away: float | None = None
    corners_home: int | None = None
    corners_away: int | None = None

    def __post_init__(self) -> None:
        for value in (self.xg_home, self.xg_away, self.possession_home, self.possession_away):
            if value is not None and value < 0:
                raise ValueError("statistic values cannot be negative")
        if self.possession_home is not None and self.possession_home > 100:
            raise ValueError("home possession cannot exceed 100")
        if self.possession_away is not None and self.possession_away > 100:
            raise ValueError("away possession cannot exceed 100")

    @property
    def has_xg(self) -> bool:
        return self.xg_home is not None and self.xg_away is not None
