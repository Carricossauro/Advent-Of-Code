# Part 2

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
			nextList = caves.copy()
			nextList.append(candidate)
			if candidate not in caves:
				print(cave, candidate)
				queue.append(nextList)
			elif candidate.isupper():
				print(cave, candidate)
				queue.append(nextList)
			elif candidate not in ['start', 'end'] and caves.count(candidate) < 2 and all([caves.count(i) < 2 for i in dest if i.islower() and i not in ['start', 'end', candidate]]):  # candidate is already lower
				print(cave, candidate)
				queue.append(nextList)

print(final)
print(len(final))
'''
final_filtered = []
for f in final:
	print("".join(f))
	if f not in final_filtered:
		final_filtered.append(f)

print(len(final_filtered))'''