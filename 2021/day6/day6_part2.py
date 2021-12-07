# Part 1

file = open("day6_part1.txt",'r')

fishes = list(map(int, file.readline()[:-1].split(',')))

print(fishes)

states = {
	0:0,
	1:0,
	2:0,
	3:0,
	4:0,
	5:0,
	6:0,
	7:0,
	8:0
}

for number in fishes:
	states[number] += 1

for _ in range(256):
	new = states[0]
	for i in range(8):
		states[i] = states[i+1]
	states[8] = new
	states[6] += new
	print(states)

print(states)
print(sum(map(lambda x: states[x] ,states)))