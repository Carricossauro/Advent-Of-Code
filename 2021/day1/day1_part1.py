# Part 1

file = open("day1.txt", 'r')
depth = None
increases = 0

for line in file.readlines():
	if depth == None:
		depth = int(line)
	elif depth < int(line):
		increases += 1
	depth = int(line)

print(increases)