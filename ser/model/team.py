from dataclasses import dataclass
from typing import List, Optional

from ser.model import Game


@dataclass
class Team:
    name: str
    games: List[Game]
    rating: Optional[float] = None
    off_rating: Optional[float] = None
    def_rating: Optional[float] = None