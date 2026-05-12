"""Data models for live football matches."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class MatchStatus(Enum):
    """Current state of a match."""

    SCHEDULED = "scheduled"
    FIRST_HALF = "1H"
    HALF_TIME = "HT"
    SECOND_HALF = "2H"
    FINISHED = "FT"
    POSTPONED = "postponed"


@dataclass(frozen=True)
class LiveMatch:
    """A single live football match."""

    home_team: str
    away_team: str
    score_home: int = 0
    score_away: int = 0
    minute: int = 0
    status: MatchStatus = MatchStatus.SCHEDULED
    league: str | None = None
    external_id: str = field(default="")

    @property
    def score(self) -> str:
        return f"{self.score_home}:{self.score_away}"

    @property
    def is_live(self) -> bool:
        return self.status in (
            MatchStatus.FIRST_HALF,
            MatchStatus.SECOND_HALF,
            MatchStatus.HALF_TIME,
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "home_team": self.home_team,
            "away_team": self.away_team,
            "score_home": self.score_home,
            "score_away": self.score_away,
            "score": self.score,
            "minute": self.minute,
            "status": self.status.value,
            "league": self.league,
            "external_id": self.external_id,
        }
