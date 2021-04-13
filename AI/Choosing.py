from math import exp
from random import random, choice


# time consuming?
# candidates is a candid->val dictionary
def soft_max_choose(candidates):
	total = 0
	for x in candidates:
		total += exp(candidates[x])
	rnd = random() * total
	for x in candidates:
		rnd -= exp(candidates[x])
		if rnd < 0:
			return x
	assert False


def max_choose(candidates):
	max_val = None
	max_candidates = []
	for x in candidates:
		if max_val is None or max_val < candidates[x]:
			max_val = candidates[x]
			max_candidates = []
		if max_val == candidates[x]:
			max_candidates.append(x)
	return choice(max_candidates)
