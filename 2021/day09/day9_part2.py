# Part 2
from functools import reduce

file = open("day9_part1.txt", 'r')

matrix = []

lines = file.readlines()

for line in lines:
	matrix.append(list(map(int, line[:-1])))

queue = []
M = len(matrix[0])
N = len(matrix)

for x in range(N):
	for y in range(M):
		adjacents = []
		if y+1 < M:
			adjacents.append((x, y+1))
		if y > 0:
			adjacents.append((x, y-1))
		if x+1 < N:
			adjacents.append((x+1, y))
		if x > 0:
			adjacents.append((x-1,y))

		if matrix[x][y] < min(map(lambda t: matrix[t[0]][t[1]], adjacents)):
			print(adjacents)
			for i,j in adjacents:
				queue.append((i,j,x,y))

basinSize = {}
for x,y, basinX, basinY in queue:
	basinSize[(basinX,basinY)] = 1

for (x, y, basinX, basinY) in queue:
	if matrix[x][y] == 9 or (x == basinX and y == basinY):
		continue
	print((x, y, basinX, basinY))
	if 0 <= x < N and 0 <= y < M:
		basinSize[basinX, basinY] += 1
	adjacents = []
	if y+1 < M:
		adjacents.append((x,y+1))
	if y > 0:
		adjacents.append((x, y-1))
	if x+1 < N:
		adjacents.append((x+1, y))
	if x > 0:
		adjacents.append((x-1, y))
	for i,j in adjacents:
		if (i, j, basinX, basinY) not in queue:
			queue.append((i, j, basinX, basinY))

print(basinSize)
basins = list(basinSize.values())
basins.sort(reverse=True)
print(reduce(lambda x,y: x*y, basins[:3]))