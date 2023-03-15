import datetime
from abc import ABC
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional


class Result(Enum):
    WIN = "WIN"
    LOSS = "LOSS"
    TIE = "TIE"
    SCHEDULED = "SCHEDULED"
    DELAYED = "DELAYED"
    CANCELED = "CANCELED"


class Location(Enum):
    HOME = -1
    AWAY = 1
    NEUTRAL = 0


@dataclass
class Game(ABC):
    team: str
    opponent: str
    result: Result
    location: Location
    date: datetime.date
    points: int = None
    opp_points: int = None
    overtimes: int = 0
    efficiency: int = None
    offensive_efficiency: int = None
    defensive_efficiency: int = None
    opp_efficiency: int = None
    opp_offensive_efficiency: int = None
    opp_defensive_efficiency: int = None

    @property
    def scoring_margin(self):
        return self.points - self.opp_points

    @property
    def completed(self):
        return self.result in [Result.WIN, Result.LOSS, Result.TIE]

    def __repr__(self) -> str:
        return f"[{self.date}] " \
            f"{self.team}{f' {self.points}' if self.points else ''} - " \
            f"{f'{self.opp_points} ' if self.opp_points else ''}{self.opponent} " \
            f"{'' if not self.overtimes else f'({self.overtimes if self.overtimes != 1 else str()}OT) '}" \
            f"[{self.location.value}]"
