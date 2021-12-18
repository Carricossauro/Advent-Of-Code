# Part 2

def print_matrix(points):
	Xmax = max(map(lambda p: p[0], points))
	Ymax = max(map(lambda p: p[1], points))
	maxPos = (Xmax, Ymax)

	for y in range(Ymax+1):
		for x in range(Xmax+1):
			if (x,y) in points:
				print('#', end="")
			else:
				print(' ', end="")
		print()

file = open("day13.txt", 'r')
#file = open("teste", 'r')

lines = file.readlines()

points = set()
folds = []
for i, line in enumerate(lines):
	if line == '\n':
		folds = [tuple(p.strip().split(' ')[2].split('=')) for p in lines[i+1:]]
		break
	else:
		points.add(tuple(map(int, line[:-1].split(','))))

Xmax = max(map(lambda p: p[0], points))
Ymax = max(map(lambda p: p[1], points))

for fold in folds:
	newPoints = set()
	values = {'x': 0, 'y': 1}
	for pos in points:
		coordinate = values[fold[0]]
		if pos[coordinate] > int(fold[1]):
			newPos = [pos[0], pos[1]]
			newPos[coordinate] = int(fold[1]) - (pos[coordinate] - int(fold[1]))
			newPoints.add(tuple(newPos))
			if coordinate == 0:
				Xmax = int(fold[1]) - 1
			else:
				Ymax = int(fold[1]) - 1
		elif pos[coordinate] < int(fold[1]):
			newPoints.add(pos)

	points = newPoints

print_matrix(points)




#print(points, len(points))
#print(newPoints, len(newPoints))
#print(folds)