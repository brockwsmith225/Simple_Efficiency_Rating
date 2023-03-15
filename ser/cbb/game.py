import dataclasses
import datetime
from dataclasses import dataclass
from typing import Optional, Union, get_args

from ser.model import Game, Location, Result


@dataclass
class CBBGame(Game):
    field_goals_made: int = None
    field_goals_attempted: int = None
    three_point_field_goals_made: int = None
    three_point_field_goals_attempted: int = None
    free_throws_made: int = None
    free_throws_attempted: int = None
    offensive_rebounds: int = None
    defensive_rebounds: int = None
    rebounds: int = None
    assists: int = None
    turnovers: int = None
    steals: int = None
    blocks: int = None
    fouls: int = None
    disqualifications: int = None
    technical_fouls: int = None
    opp_field_goals_made: int = None
    opp_field_goals_attempted: int = None
    opp_three_point_field_goals_made: int = None
    opp_three_point_field_goals_attempted: int = None
    opp_free_throws_made: int = None
    opp_free_throws_attempted: int = None
    opp_offensive_rebounds: int = None
    opp_defensive_rebounds: int = None
    opp_rebounds: int = None
    opp_assists: int = None
    opp_turnovers: int = None
    opp_steals: int = None
    opp_blocks: int = None
    opp_fouls: int = None
    opp_disqualifications: int = None
    opp_technical_fouls: int = None

    def __post_init__(self):
        for field in dataclasses.fields(self):
            value = getattr(self, field.name)
            if value is None:
                continue
            if field.type == Location:
                if value == "home":
                    setattr(self, field.name, Location.HOME)
                elif value == "away":
                    setattr(self, field.name, Location.AWAY)
                elif value == "neutral":
                    setattr(self, field.name, Location.NEUTRAL)
            elif field.type == Result:
                if value == "W":
                    setattr(self, field.name, Result.WIN)
                elif value == "L":
                    setattr(self, field.name, Result.LOSS)
            elif field.type == datetime.date:
                setattr(self, field.name, datetime.datetime.strptime(value, "%m/%d/%Y").date())
            elif field.type == Union:
                setattr(self, field.name, get_args(field.type)[0](value))
            else:
                setattr(self, field.name, field.type(value))

    @property
    def adj_reg_points(self):
        return (self.points * (8 / (8 + self.overtimes)))

    @property
    def adj_reg_opp_points(self):
        return (self.opp_points * (8 / (8 + self.overtimes)))

    @property
    def possessions(self) -> float:
        return self.field_goals_attempted - self.offensive_rebounds + self.turnovers + self.free_throws_attempted * 0.44  # 0.44 comes from true shooting percentage, just trust it

    @property
    def opp_possessions(self) -> float:
        return self.opp_field_goals_attempted - self.opp_offensive_rebounds + self.opp_turnovers + self.opp_free_throws_attempted * 0.44  # 0.44 comes from true shooting percentage, just trust it

    @property
    def points_per_possession(self) -> float:
        return float(self.points) / self.possessions

    @property
    def opp_points_per_possession(self) -> float:
        return float(self.opp_points) / self.opp_possessions
