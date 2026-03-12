import math
from typing import Optional

from ratingsystems import Rating, RatingSystem, Stat, TeamRating

from ratingsystems.ser.model import Efficiency


class SimpleEfficiencyRatingSystem(RatingSystem):

    class Meta:
        name: str = "ser"
    
    def __init__(self, k: float = 1.0):
        self.k = k

    def rate(self, games: list, seed: Rating = None) -> Rating:
        if seed is not None:
            seed = Rating.minmax_normalize(seed)

        points = {}
        points_against = {}
        for game in games:
            if isinstance(game, tuple):
                winner = game[0]
                loser = game[1]
                winner_points = game[2]
                loser_points = game[3]
            else:
                # if not game.completed:
                #     continue
                # if game.home_division not in ["fbs"]:
                #     game.home_team = "exclude"
                #     continue
                # if game.away_division not in ["fbs"]:
                #     game.away_team = "exclude"
                #     continue
                if game.home_team not in points:
                    points[game.home_team] = []
                    points_against[game.home_team] = []
                if game.away_team not in points:
                    points[game.away_team] = []
                    points_against[game.away_team] = []
                points[game.home_team].append((game.home_points, game.away_team))
                points_against[game.home_team].append((game.away_points, game.away_team))
                points[game.away_team].append((game.away_points, game.home_team))
                points_against[game.away_team].append((game.home_points, game.home_team))

        global_points = [value[0] for team in points for value in points[team]]
        global_avg_points = self._safe_divide(sum(global_points), len(global_points))

        avg_points = {t: self._safe_divide(sum([p for p, _ in games]), len(games)) for t, games in points.items()}
        avg_points_against = {t: self._safe_divide(sum([p for p, _ in games]), len(games)) for t, games in points_against.items()}
        offensive_efficiencies = {t: [(self._calculate_offensive_efficiency(p, avg_points_against[opp]), opp) for p, opp in games] for t, games in points.items()}
        defensive_efficiencies = {t: [(self._calculate_defensive_efficiency(p, avg_points[opp]), opp) for p, opp in games] for t, games in points_against.items()}
        if seed is not None:
            offensive_efficiency = Rating({t: Efficiency(self._safe_divide(sum([e * seed.get_rating(opp, 0) for e, opp in games]), sum([seed.get_rating(opp, 0) for _, opp in games]))) for t, games in offensive_efficiencies.items()}, name="_efficiency", games=games, points_mode=PointsMode.FOR, _k=self.k)
            defensive_efficiency = Rating({t: Efficiency(self._safe_divide(sum([e * seed.get_rating(opp, 0) for e, opp in games]), sum([seed.get_rating(opp, 0) for _, opp in games]))) for t, games in defensive_efficiencies.items()}, name="_efficiency", games=games, points_mode=PointsMode.AGAINST, _k=self.k)
            # offensive_ratings = {t: self._safe_divide(sum([e * (seed.get_rating(opp, 0) if e > 0 else 1 - seed.get_rating(opp, 0)) for e, opp in games]), sum([(seed.get_rating(opp, 0) if e > 0 else 1 - seed.get_rating(opp, 0)) for e, opp in games])) for t, games in offensive_efficiencies.items()}
            # defensive_ratings = {t: self._safe_divide(sum([e * (seed.get_rating(opp, 0) if e > 0 else 1 - seed.get_rating(opp, 0)) for e, opp in games]), sum([(seed.get_rating(opp, 0) if e > 0 else 1 - seed.get_rating(opp, 0)) for e, opp in games])) for t, games in defensive_efficiencies.items()}
        else:
            offensive_efficiency = Rating({t: Efficiency(self._safe_divide(sum([e for e, _ in games]), len(games))) for t, games in offensive_efficiencies.items()}, name="_efficiency", games=games, _k=self.k)
            defensive_efficiency = Rating({t: Efficiency(self._safe_divide(sum([e for e, _ in games]), len(games))) for t, games in defensive_efficiencies.items()}, name="_efficiency", games=games, _k=self.k)

        offensive_rating = Rating({t: Stat(self._calculate_points_from_offensive_efficiency(offensive_efficiency.get_value(t), global_avg_points)) for t in offensive_efficiency.teams()}, name="offense", games=games, _efficiency=offensive_efficiency)
        defensive_rating = Rating({t: Stat(self._calculate_points_from_defensive_efficiency(defensive_efficiency.get_value(t), global_avg_points)) for t in defensive_efficiency.teams()}, name="defense", games=games, _efficiency=defensive_efficiency)

        return (offensive_rating - defensive_rating) % "ser"

    def _calculate_offensive_efficiency(self, points: float, opp_avg_points_against: float) -> float:
        if opp_avg_points_against == 0:
            opp_avg_points_against = 1.0
        return 2 / (1 + pow(math.e, -1 * self.k / opp_avg_points_against * (points - opp_avg_points_against))) - 1

    def _calculate_defensive_efficiency(self, points: float, opp_avg_points: float) -> float:
        if opp_avg_points == 0:
            opp_avg_points = 1.0
        return 2 / (1 + pow(math.e, -1 * self.k / opp_avg_points * (opp_avg_points - points))) - 1

    def _calculate_points_from_offensive_efficiency(self, efficiency: float, avg_points: float) -> float:
        # Calculated by the inverse of the sigmoid function used in _calculate_offensive_efficiency
        return avg_points * (1 - math.log(2 / (efficiency + 1) - 1) / self.k)

    def _calculate_points_from_defensive_efficiency(self, efficiency: float, avg_points: float) -> float:
        # Calculated by the inverse of the sigmoid function used in _calculate_defensive_efficiency
        return avg_points * (1 + math.log(2 / (efficiency + 1) - 1) / self.k)

    @classmethod
    def _safe_divide(cls, x: float, y: float, default: float = 0.0) -> float:
        if y == 0:
            return default
        return x / y