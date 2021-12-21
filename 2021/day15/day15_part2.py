# Part 2

def remakeMap(oldMatrix, N):
	newMatrix = []
	for m in range(5):
		for p in range(N):
			newMatrix.append(oldMatrix[p].copy())
			for i, elem in enumerate(newMatrix[-1]):
				num = elem + m
				newMatrix[-1][i] = num if num < 10 else num - 9
			for n in range(1, 5):
				for elem in newMatrix[-1][:N]:
					num = elem + n
					newMatrix[-1].append(num if num < 10 else num - 9)

	return newMatrix

def adjacent_positions(N,M,x,y):
	lista = []
	if y > 0:
		lista.append((x, y-1)) # top-middle
	if x < N-1:
		lista.append((x+1, y)) # middle-right
	if y < M-1:
		lista.append((x, y+1)) # bottom-middle
	if x > 0:
		lista.append((x-1, y)) # middle-left
	return lista

file = open("day15.txt", 'r')
#file = open("teste", 'r')

oldMatrix = list(map(lambda pos: list(map(int, pos[:-1])), file.readlines()))

matrix = remakeMap(oldMatrix, len(oldMatrix))
N = len(matrix)
lastPos = (N-1, N-1)

for p in matrix:
	print("".join(map(str,p)))

risks = {}
maxMovements = 3 * N

# initialize dynamic programming table
risks[0] = {}
for x in range(N):
	for y in range(N):
		risks[0][(x,y)] = float("inf")

risks[0][(0,0)] = 0

# calculate the rest of the table
for m in range(1, maxMovements):
	risks[m] = {}
	for x in range(N):
		for y in range(N):
			previousRisks = [risks[m-1][candidate] for candidate in adjacent_positions(N,N,x,y)]
			if previousRisks == []:
				risks[m][(x,y)] = float("inf")
			else:
				risks[m][(x,y)] = min(previousRisks) + matrix[y][x]

print(min([risks[m][lastPos] for m in range(maxMovements)]))