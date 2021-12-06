# Part 2

# co2
file = open("day3_part2.txt",'r')
lines = file.readlines()

for pos in range(len(lines[0])-1):
	if len(lines) <= 1:
		break
	freq = [0,0]
	for line in lines:
		freq[int(line[pos])] += 1
	f = 0
	if freq[0] > freq[1]:
		f = 1
	lines = list(filter(lambda x: int(x[pos]) == f, lines))

co2 = lines[0][:-1]
file.close()

# oxygen
file = open("day3_part2.txt",'r')
lines = file.readlines()

for pos in range(len(lines[0])-1):
	if len(lines) <= 1:
		break
	freq = [0,0]
	for line in lines:
		freq[int(line[pos])] += 1
	f = 0
	if freq[0] <= freq[1]:
		f = 1
	lines = list(filter(lambda x: int(x[pos]) == f, lines))

oxygen = lines[0][:-1]
file.close()

print(co2, oxygen)
co2 = co2[::-1]
oxygen = oxygen[::-1]

co2_soma = 0
oxygen_soma = 0
exp = 0

for p in range(len(co2)):
	co2_soma += int(co2[p]) * 2**exp
	oxygen_soma += int(oxygen[p]) * 2**exp
	exp += 1

print(co2_soma, oxygen_soma)

print(co2_soma * oxygen_soma)