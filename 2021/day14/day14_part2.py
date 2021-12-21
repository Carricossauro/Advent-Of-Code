# Part 2

import collections

def step(rules, frequencies, pairs):
	pairList = list(pairs.items())
	for pair, freq in pairList:
		if pair in rules:
			x, y = pair
			newElem = rules[pair]
			pairs[pair] -= freq
			if (x, newElem) not in pairs:
				pairs[(x, newElem)] = 0
			if (newElem, y) not in pairs:
				pairs[(newElem, y)] = 0
			pairs[(x, newElem)] += freq
			pairs[(newElem, y)] += freq
			if newElem not in frequencies:
				frequencies[newElem] = 0
			frequencies[newElem] += freq

	return frequencies, pairs

file = open("day14.txt", 'r')

lines = file.readlines()

polymer = lines[0].strip()
rules = dict([((k[0], k[1]), v) for k, v in map(lambda x: tuple(x.strip().split(" -> ")),lines[2:])])

frequencies = {}
pairs = {}

for i, elem in enumerate(polymer):
	if elem not in frequencies:
		frequencies[elem] = 0
	frequencies[elem] += 1
	if i > 0:
		pair = (polymer[i-1], elem)
		if pair not in pairs:
			pairs[pair] = 0
		pairs[pair] += 1

print(polymer)
print(frequencies)
print(pairs)
print(rules)

for _ in range(40):
	frequencies, pairs = step(rules, frequencies, pairs)

print("frequencies", frequencies)
print("pairs", pairs)
print("rules", rules)

frequencyList = frequencies.values()
print(max(frequencyList) - min(frequencyList))