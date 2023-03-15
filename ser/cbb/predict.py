from csv import DictReader
import math
from statistics import stdev
from typing import Dict, List, Tuple

from ser.model import Bracket, Factors, Location, Prediction
from ser.util import math as m
from ser.cbb.rank import calculate_efficiencies
from ser.cbb.team import CBBTeam


def predict_game(teams: Dict[str, CBBTeam], team: str, opponent: str, location: Location, factors: Factors) -> List[Tuple[str, float]]:
    a = teams[team]
    b = teams[opponent]

    calculate_efficiencies(teams, a, factors)
    calculate_efficiencies(teams, b, factors)

    a_points = (a.offensive_efficiency * b.opp_points_per_possession + a.points_per_possession / b.defensive_efficiency) / 2 + a.points_per_possession_stddev * a.offensive_efficiency / b.defensive_efficiency
    a_points_stddev = a.points_per_possession_stddev
    b_points = (b.offensive_efficiency * a.opp_points_per_possession + b.points_per_possession / a.defensive_efficiency) / 2 + b.points_per_possession_stddev * b.offensive_efficiency / a.defensive_efficiency
    b_points_stddev = b.points_per_possession_stddev
    pace = (a.possessions_per_game / a.possessions_per_game_stddev + b.possessions_per_game / b.possessions_per_game_stddev) / (1.0 / a.possessions_per_game_stddev + 1.0 / b.possessions_per_game_stddev)

    line = (b_points - a_points) * pace
    stddev = math.sqrt(pow(a_points_stddev * pace, 2) + pow(b_points_stddev * pace, 2))
    odds = m.cdf(0.0, line, stddev)

    return Prediction(
        team=team,
        opponent=opponent,
        predicted_points=a_points * pace,
        opp_predicted_points=b_points * pace,
        odds=odds,
    )


def predict_bracket(teams: Dict[str, CBBTeam], bracket: Bracket, factors: Factors) -> List:
    path = f"./warner_score.csv"
    teams = dict()
    warner_scores = []
    with open(path, "r") as f:
        csv_dict_reader = DictReader(f)
        for row in csv_dict_reader:
            teams[row["team"]] = float(row["warner_score"])
            if teams[row["team"]] > 1000:
                warner_scores.append(float(row["warner_score"]))
    std_dev_warner = stdev(warner_scores)
    def predictor(team_1: str, team_2: str, location: Location) -> float:
        diff = teams[team_1] - teams[team_2]
        return 1.0/(1 + pow(10, -diff/std_dev_warner))

    bracket.evaluate(predictor)

    print(bracket)
    bracket_odds = []
    for team, bracket, seed, odds in bracket.full_odds.values():
        bracket_odds.append((team, bracket, seed, teams[team], odds))
    return bracket_odds
