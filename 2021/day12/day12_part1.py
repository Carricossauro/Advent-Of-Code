# Part 1

file = open("day12.txt", 'r')

dest = {}

for line in file.readlines():
	caves = line.split('-')
	caves[1] = caves[1][:-1]
	if caves[0] not in dest:
		dest[caves[0]] = []
	if caves[1] not in dest:
		dest[caves[1]] = []
	dest[caves[0]].append(caves[1])
	dest[caves[1]].append(caves[0])
	print(caves)
print(dest)

final = []

queue = [["start"]]
for caves in queue:
	cave = caves[-1]
	if cave == 'end':
		final.append(caves)
	else:
		candidates = dest[cave]
		for candidate in candidates:
			if candidate not in caves:
				print(cave, candidate)
				nextList = caves.copy()
				nextList.append(candidate)
				queue.append(nextList)
			elif candidate.isupper():
				print(cave, candidate)
				nextList = caves.copy()
				nextList.append(candidate)
				queue.append(nextList)

print(final)
print(len(final))