from dataclasses import dataclass
from statistics import stdev
from typing import Optional

from ser.model import Team
from ser.model import Result


@dataclass
class CBBTeam(Team):
    efficiency: Optional[int] = None
    offensive_efficiency: Optional[int] = None
    defensive_efficiency: Optional[int] = None
    opp_efficiency: Optional[int] = None
    opp_offensive_efficiency: Optional[int] = None
    opp_defensive_efficiency: Optional[int] = None

    @property
    def wins(self) -> int:
        return sum([1 if g.result == Result.WIN else 0 for g in self.games])

    @property
    def losses(self) -> int:
        return sum([1 if g.result == Result.LOSS else 0 for g in self.games])

    @property
    def num_of_games(self) -> int:
        return len([1 for g in self.games if g.completed])

    @property
    def points_per_game(self) -> float:
        return sum([float(g.points) for g in self.games if g.completed]) / self.num_of_games

    @property
    def points_per_game_stddev(self) -> float:
        return stdev([float(g.points) for g in self.games if g.completed])

    @property
    def opp_points_per_game(self) -> float:
        return sum([float(g.opp_points) for g in self.games if g.completed]) / self.num_of_games

    @property
    def opp_points_per_game_stddev(self) -> float:
        return stdev([float(g.opp_points) for g in self.games if g.completed])

    @property
    def possessions_per_game(self) -> float:
        return sum([float(g.possessions) for g in self.games if g.completed]) / self.num_of_games

    @property
    def possessions_per_game_stddev(self) -> float:
        return stdev([float(g.possessions) for g in self.games if g.completed]) / self.num_of_games

    @property
    def points_per_possession(self) -> float:
        return sum([float(g.points) for g in self.games if g.completed]) / sum([float(g.possessions) for g in self.games if g.completed])

    @property
    def points_per_possession_stddev(self) -> float:
        return stdev([float(g.points) / float(g.possessions) for g in self.games if g.completed])

    @property
    def opp_possessions_per_game(self) -> float:
        return sum([float(g.opp_possessions) for g in self.games if g.completed]) / self.num_of_games

    @property
    def opp_possessions_per_game_stddev(self) -> float:
        return stdev([float(g.opp_possessions) for g in self.games if g.completed]) / self.num_of_games

    @property
    def opp_points_per_possession(self) -> float:
        return sum([float(g.opp_points) for g in self.games if g.completed]) / sum([float(g.opp_possessions) for g in self.games if g.completed])

    @property
    def opp_points_per_possession_stddev(self) -> float:
        return stdev([float(g.opp_points) / float(g.opp_possessions) for g in self.games if g.completed])

