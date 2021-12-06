# Part 2

file = open("day1_part2.txt", 'r')
increases = 0
sums = []

for line in file.readlines():
	sums.append(int(line))
	if len(sums) >= 2:
		sums[-2] += int(line)
	if len(sums) >= 3:
		sums[-3] += int(line)
	print(line, sums)

depth = sums[0]

for x in sums[1:-2]:
	if x > depth:
		increases += 1
	depth = x

print(increases)