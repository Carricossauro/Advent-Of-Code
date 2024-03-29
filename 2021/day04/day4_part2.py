# Part 2

def replace(matrix, number):
	N = len(matrix)
	for i in range(N):
		for j in range(N):
			if matrix[i][j][1] == number:
				matrix[i][j] = (True, number)
				return True
	return False

def gameOver(matrix):
	N = len(matrix)
	for i in range(N):
		if all(map(lambda x: x[0], matrix[i])):
			return True
		if all(map(lambda x: x[0], [matrix[y][i] for y in range(N)])):
			return True

	return False

file = open("day4.txt", 'r')

bingo = list(map(int, file.readline().strip().split(',')))
print(bingo)

matrix = {}
matrix[1] = []
i = 1

token = file.readline()
token = file.readline()

while token:
	if token == '\n':
		i += 1
		matrix[i] = []
	else:
		line = token[:-1]
		lista = line.split()
		matrix[i].append(list(map(lambda x: (False, int(x)), lista)))

	token = file.readline()

file.close()
# File reading over
# Starting bingo number reading

N = len(matrix)
over = []
loser = -1

for number in bingo:
	for pos in range(1, N+1):
		if pos not in over:
			replace(matrix[pos], number)
			if gameOver(matrix[pos]):
				over.append(pos)
				if len(over) == N:
					loser = pos
					break
	if loser != -1:
		break

sumUnmarked = 0
M = len(matrix[loser])

for i  in range(M):
	print(i, matrix[loser][i])
	for j in range(M):
		if not matrix[loser][i][j][0]:
			sumUnmarked += matrix[loser][i][j][1]

print("Loser: " + str(loser))
print(sumUnmarked)
print(number)

print(sumUnmarked * number)