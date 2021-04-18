from math import exp
from random import random, choice


# time consuming?
# candidates is a candid->val dictionary
def soft_max_choose(candidates):
	max_score = None
	for x in candidates:
		if max_score is None or max_score < candidates[x]:
			max_score = candidates[x]
	total = 0
	for x in candidates:
		total += exp(candidates[x]-max_score)
	rnd = random() * total
	for x in candidates:
		rnd -= exp(candidates[x]-max_score)
		if rnd <= float(1e-5):
			return x
	assert False


def max_choose(candidates):
	max_val = None
	max_candidates = []
	for x in candidates:
		if max_val is None or max_val < candidates[x]:
			max_val = candidates[x]
	eps = 0.00001
	for x in candidates:
		if abs(max_val-candidates[x]) <= eps:
			max_candidates.append(x)
	# print("scores : ", end = '')
	# for x in candidates:
	# 	print(x, "->", candidates[x], end = " ")
	# print()
	return choice(max_candidates)
