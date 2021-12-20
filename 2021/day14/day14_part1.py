# Part 1

import collections

def step(rules, polymer):
	pairs = []
	for i in range(len(polymer)-1):
		pairs.append("".join([polymer[i], polymer[i+1]]))

	newPolymer = []
	for i, pair in enumerate(pairs):
		if i == 0:
			newPolymer.append(pair[0])

		if pair in rules:
			newPolymer.append(rules[pair])
			newPolymer.append(pair[1])
		elif i == len(polymer) - 1:
			newPolymer.append(pair[1])
	return "".join(newPolymer)

file = open("day14.txt", 'r')

lines = file.readlines()

polymer = lines[0].strip()
rules = dict(map(lambda x: tuple(x.strip().split(" -> ")),lines[2:]))

for _ in range(10):
	polymer = step(rules, polymer)

print(polymer)

frequencies = dict(collections.Counter(polymer)).values()
print(max(frequencies) - min(frequencies))