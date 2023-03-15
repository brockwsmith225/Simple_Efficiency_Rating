from typing import Dict, List, Tuple

from ser.model import Factors
from ser.util import math as m
from ser.cbb.team import CBBTeam


def calculate_efficiencies(teams: Dict[str, CBBTeam], team: CBBTeam, factors: Factors):
	if team.efficiency is not None:
		return

	team.offensive_efficiency = 1.0
	team.defensive_efficiency = 1.0

	adj_game_count = 0.0
	for game in team.games:
		if game.opponent not in teams:
			continue
		# Set game efficiencies
		game.offensive_efficiency = m.safe_division(game.points_per_possession, teams[game.opponent].opp_points_per_possession, 1.0)
		game.defensive_efficiency = m.safe_division(teams[game.opponent].points_per_possession, game.opp_points_per_possession, 1.0)
		game.efficiency = game.offensive_efficiency * game.defensive_efficiency

		# Set team efficiencies
		location_weight = (1 + game.location.value * factors.location) / max(1 + factors.location, 1 - factors.location)
		game_weight = location_weight
		team.offensive_efficiency *= pow(game.offensive_efficiency, game_weight)
		team.defensive_efficiency *= pow(game.defensive_efficiency, game_weight)
		adj_game_count += game_weight

	team.offensive_efficiency = pow(team.offensive_efficiency, 1.0 / adj_game_count)
	team.defensive_efficiency = pow(team.defensive_efficiency, 1.0 / adj_game_count)
	team.efficiency = team.offensive_efficiency * team.defensive_efficiency


def rank_teams(teams: Dict[str, CBBTeam], factors: Factors) -> List[Tuple[str, float]]:
	rankings = list()

	for team in teams.values():

		calculate_efficiencies(teams, team, factors)
		rankings.append((team.name, team.efficiency))

	return reversed(sorted(rankings, key=lambda t: t[1]))
