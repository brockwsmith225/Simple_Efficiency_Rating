from dataclasses import dataclass


@dataclass
class Prediction:
	team: str
	opponent: str
	predicted_points: float
	opp_predicted_points: float
	odds: float

	@property
	def line(self):
		return self.opp_predicted_points - self.predicted_points

	def __repr__(self):
		return f"{self.team} {'{odds:.2f}'.format(odds=self.odds * 100)}% ({round(self.predicted_points)}) - ({round(self.opp_predicted_points)}) {'{odds:.2f}'.format(odds=(1 - self.odds) * 100)}% {self.opponent}"
