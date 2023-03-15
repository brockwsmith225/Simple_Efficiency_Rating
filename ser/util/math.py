import math


def safe_division(a: float, b: float, undefined: float = 0.0) -> float:
	if b != 0:
		return a / b
	return undefined


def pdf(x: float):
	return math.exp(-x * x / 2) / math.sqrt(2 * math.pi)


def cdf(z: float, mu: float = 0.0, sigma: float = 1.0) -> float:
	z = (z - mu) / sigma
	if z < -8.0:
		return 0.0
	if z > 8.0:
		return 1.0
	total = 0.0
	term = z
	i = 3
	while total + term != total:
		total += term
		term = term * z * z / i
		i += 2
	return 0.5 + total * pdf(z)
