# Part 2

file = open("day5_part2.txt", 'r')

line = file.readline()
lista = []

while line:
	lista.append(tuple(map(lambda x: tuple(map(int, x.strip().split(','))), line.split('->'))))
	line = file.readline()

file.close()
# File reading over

matrix = {}

for x,y in lista:
	if x[0] == y[0] or x[1] == y[1]:
		for X in range(min(x[0], y[0]), max(x[0], y[0]) + 1):
			for Y in range(min(x[1], y[1]), max(x[1], y[1]) + 1):
				if (Y,X) not in matrix:
					matrix[(Y,X)] = 0
				matrix[(Y,X)] += 1
	else:
		difX = 1 if (y[0] > x[0]) else -1
		difY = 1 if (y[1] > x[1]) else -1
		X = x[0]
		Y = x[1]
		while True:
			if (Y,X) not in matrix:
				matrix[(Y,X)] = 0
			matrix[(Y,X)] += 1
			X += difX
			Y += difY
			if X == y[0] and Y == y[1]:
				if (Y,X) not in matrix:
					matrix[(Y,X)] = 0
				matrix[(Y,X)] += 1
				break

sumOverlaps = 0

for pair in matrix:
	if matrix[pair] >= 2:
		sumOverlaps += 1

print(sumOverlaps)

'''
for x in range(10):
	for y in range(10):
		if (x,y) in matrix:
			print(f"{matrix[(x,y)]}", end="")
		else:
			print('.', end="")
	print()
'''