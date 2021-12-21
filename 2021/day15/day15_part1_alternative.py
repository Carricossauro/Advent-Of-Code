# Part 1 Alternative
# Alternative version using a graph/dynamic programming hybrid
# this would be much easier if I knew dynamic programming :(

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

matrix = list(map(lambda pos: list(map(int, pos[:-1])), file.readlines()))

N = len(matrix)
lastPos = (N-1, N-1)

minimumRisk = {}
for x in range(N):
	for y in range(N):
		minimumRisk[(x,y)] = float("inf")

queue = [(0, 0, 0)] # x, y, risk
minimumRisk[(0,0)] = 0

for x, y, risk in queue:
	if (x,y) != lastPos:
		candidates = adjacent_positions(N, N, x, y)
		for candidate in candidates:
			X = candidate[0]
			Y = candidate[1]
			newRisk = risk + matrix[Y][X]
			if newRisk < minimumRisk[(X,Y)]:
				minimumRisk[(X,Y)] = newRisk
				queue.append( (X, Y, newRisk) )

# print(matrix, N)
print(minimumRisk[lastPos])
