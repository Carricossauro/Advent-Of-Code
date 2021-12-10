# Part 1

file = open("day9_part1.txt",'r')

matrix = []

lines = file.readlines()

for line in lines:
	matrix.append(list(map(int, line[:-1])))

lista = []
M = len(matrix[0])
N = len(matrix)
for x in range(N):
	for y in range(M):
		adjacents = []
		if y+1 < M:
			adjacents.append(matrix[x][y+1])
		if y > 0:
			adjacents.append(matrix[x][y-1])
		if x+1 < N:
			adjacents.append(matrix[x+1][y])
		if x > 0:
			adjacents.append(matrix[x-1][y])

		if matrix[x][y] < min(adjacents):
			lista.append(matrix[x][y])

print(lista)
print(sum(lista) + len(lista))