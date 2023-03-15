from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

from ser.model.game import Location


@dataclass
class Bracket:
	subbracket_1: Optional[Any]
	subbracket_2: Optional[Any]
	seed_1: Optional[int] = None
	seed_2: Optional[int] = None
	odds: Dict[str, float] = None
	bracket_name: str = ""
	location: Location = Location.NEUTRAL

	@property
	def depth(self) -> int:
		depth = 0
		if self.subbracket_1 is not None:
			if isinstance(self.subbracket_1, str):
				depth = 1
			else:
				depth = 1 + self.subbracket_1.depth
		if self.subbracket_2 is not None:
			if isinstance(self.subbracket_2, str):
				depth = max(1, depth)
			else:
				depth = max(1 + self.subbracket_2.depth, depth)
		return depth

	@property
	def teams(self) -> List[str]:
		teams = []
		if self.depth == 1:
			if self.subbracket_1 is not None:
				teams.append(self.subbracket_1)
			if self.subbracket_2 is not None:
				teams.append(self.subbracket_2)
		else:
			return self.subbracket_1.teams + self.subbracket_2.teams
		return teams

	@property
	def predicted_team(self) -> str:
		if not self.odds:
			return
		k = list(self.odds.keys())
		v = list(self.odds.values())
		return k[v.index(max(v))]

	def evaluate(self, predictor: Callable[[str, str], str]):
		self.odds = {}
		if self.depth == 1:
			if self.subbracket_2 is None:
				self.odds[self.subbracket_1] = 1.0
			else:
				game_odds = predictor(self.subbracket_1, self.subbracket_2, self.location)
				self.odds[self.subbracket_1] = game_odds
				self.odds[self.subbracket_2] = 1.0 - game_odds
		else:
			self.subbracket_1.evaluate(predictor)
			self.subbracket_2.evaluate(predictor)
			for team_1 in self.subbracket_1.teams:
				self.odds[team_1] = 0.0
				for team_2 in self.subbracket_2.teams:
					if not team_2 in self.odds:
						self.odds[team_2] = 0.0
					game_odds = predictor(team_1, team_2, self.location)
					self.odds[team_1] += game_odds * self.subbracket_1.odds[team_1] * self.subbracket_2.odds[team_2]
					self.odds[team_2] += (1.0 - game_odds) * self.subbracket_1.odds[team_1] * self.subbracket_2.odds[team_2]


	def __repr__(self) -> str:
		if self.depth == 1:
			if self.subbracket_2 is None:
				return f"{''.ljust(21)}\n{''.ljust(21)}\n{''.ljust(21)}"
			return f"{self.subbracket_1.ljust(20, '-')}|\n{''.ljust(20)}|\n{self.subbracket_2.ljust(20, '-')}|"
		else:
			subbracket_1_repr = self.subbracket_1.__repr__().split("\n")
			subbracket_2_repr = self.subbracket_2.__repr__().split("\n")

			middle = int(len(subbracket_1_repr) / 2)

			for i in range(middle):
				subbracket_1_repr[i] += f"{''.ljust(21)}"
			if self.subbracket_1.subbracket_2 is None:
				subbracket_1_repr[middle] += f"{self.subbracket_1.subbracket_1.ljust(20, '-')}|"
			elif self.subbracket_1.predicted_team:
				subbracket_1_repr[middle] += f"{self.subbracket_1.predicted_team.ljust(20, '-')}|"
			else:
				subbracket_1_repr[middle] += f"{''.ljust(20, '-')}|"
			for i in range(middle + 1, len(subbracket_1_repr)):
				subbracket_1_repr[i] += f"{''.ljust(20)}|"

			for i in range(pow(2, self.depth - 1)):
				subbracket_1_repr.append(f"{''.ljust(21 * self.depth - 1)}|")

			for i in range(middle):
				subbracket_2_repr[i] += f"{''.ljust(20)}|"
			if self.subbracket_2.subbracket_2 is None:
				subbracket_2_repr[middle] += f"{self.subbracket_2.subbracket_1.ljust(20, '-')}|"
			elif self.subbracket_2.predicted_team:
				subbracket_2_repr[middle] += f"{self.subbracket_2.predicted_team.ljust(20, '-')}|"
			else:
				subbracket_2_repr[middle] += f"{''.ljust(20, '-')}|"
			for i in range(middle + 1, len(subbracket_2_repr)):
				subbracket_2_repr[i] += f"{''.ljust(21)}"

			subbracket_1_repr.extend(subbracket_2_repr)
			return "\n".join(subbracket_1_repr)

