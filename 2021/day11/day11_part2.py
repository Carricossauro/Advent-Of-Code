# Part 2

def print_matrix(matrix):
	for p in matrix:
		print(p)

def adjacent_positions(N,M,x,y):
	lista = []
	if x > 0 and y > 0:
		lista.append((x-1, y-1)) # top-left
	if y > 0:
		lista.append((x, y-1)) # top-middle
	if y > 0 and x < N-1:
		lista.append((x+1, y-1)) # top-right
	if x < N-1:
		lista.append((x+1, y)) # middle-right
	if x < N-1 and y < M-1:
		lista.append((x+1, y+1)) # bottom-right
	if y < M-1:
		lista.append((x, y+1)) # bottom-middle
	if x > 0 and y < M-1:
		lista.append((x-1, y+1)) # bottom-left
	if x > 0:
		lista.append((x-1, y)) # middle-left
	return lista

def solve(matrix, N, M):
	queue = []
	for x in range(N):
		for y in range(M):
			queue.append((x,y))

	flashed = []
	for x,y in queue:
		if matrix[y][x] == 9:
			flashed.append((x,y))
			candidates = adjacent_positions(N,M,x,y)
			for pair in candidates:
				if pair not in flashed:
					queue.append(pair)
		matrix[y][x] = (matrix[y][x] + 1) % 10

	for (x,y) in flashed:
		matrix[y][x] = 0

	return len(flashed)

file = open("day11.txt",'r')

matrix = list(map(lambda line: list(map(int, line[:-1])),file.readlines()))

N = len(matrix[0]) # x
M = len(matrix) # y

total_flashes = 0
for step in range(999):
	new_flashes = solve(matrix, N, M)
	total_flashes += new_flashes
	if new_flashes == N*M:
		break
	print_matrix(matrix)

print(total_flashes)
print(step+1)