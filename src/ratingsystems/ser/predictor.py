import scipy.stats as st

from ratingsystems import Prediction, Predictor, Rating


class SimpleEfficiencyPredictor(Predictor):

    class Meta:
        name: str = "ser"

    def predict(self, team: str, opponent: str) -> Prediction:
        team_offensive_efficiency = inverse_sigmoid(self.rating.offense.efficiency.get_value(team), k=self.rating.offense.efficiency._k)
        team_defensive_efficiency = 0

        opponent_offensive_efficiency = 0
        opponent_defensive_efficiency = 0

        team_score = (team_offensive_efficiency * opponent_avg_points_allowed + opponent_defensive_efficiency * team_avg_points) / 2
        opponent_score = (opponent_offensive_efficiency * team_avg_points_allowed + team_defensive_efficiency * opponent_avg_points) / 2

        return Prediction(
            team,
            opponent,
            line=team_score - opponent_score,
            odds=st.norm.cdf((team_score - opponent_score) / self.rating.confidence_interval),
            team_score=team_score,
            opponent_score=opponent_score,
        )
