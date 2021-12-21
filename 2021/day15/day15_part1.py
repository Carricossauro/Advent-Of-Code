# Part 1

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

matrix = list(map(lambda pos: list(map(int, pos[:-1])), file.readlines()))

N = len(matrix)
lastPos = (N-1, N-1)

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