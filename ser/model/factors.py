from dataclasses import dataclass
from typing import List


@dataclass
class Factors:
	location: float = 0.0
	luck: float = 0.0

	@staticmethod
	def from_list(factors: List[str]):
		factors_dict = {}
		for f in factors:
			factor = f.split("=")
			factors_dict[factor[0].lower()] = float(factor[1])
		return Factors(**factors_dict)
