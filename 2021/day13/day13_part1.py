# Part 1

file = open("day13.txt", 'r')

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
maxPos = (Xmax, Ymax)
newPoints = set()
values = {'x': 0, 'y': 1}
fold = folds[0]
for pos in points:
	if pos[values[fold[0]]] > int(fold[1]):
		newPos = [pos[0], pos[1]]
		newPos[values[fold[0]]] = maxPos[values[fold[0]]] - pos[values[fold[0]]]
		newPoints.add(tuple(newPos))
	else:
		newPoints.add(pos)

print(points, len(points))
print(newPoints, len(newPoints))
#print(folds)