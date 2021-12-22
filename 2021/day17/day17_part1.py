# Part 1

# velocity: (x, y)
# x_bounds: (min, max)
# y_bounds: (min, max)
def trajectory(velocity, x_bounds, y_bounds):
	# Starting position is always (0,0)
	# List of positions (x, y) in the probe's trajectory
	positionList = [(0,0)]

	# "Graph style" position calculations
	for x, y in positionList:
		if velocity['x'] == 0 and y < y_bounds[0]:
			return positionList[:-1]

		# Calculate new position based on current position and velocity
		newPosition_x = x + velocity['x']
		newPosition_y = y + velocity['y']
		positionList.append( (newPosition_x, newPosition_y) )

		# Changes to the velocity as explained in problem
		if velocity['x'] != 0:
			velocity['x'] += 1 if velocity['x'] < 0 else -1
		velocity['y'] -= 1

	return []

# Open and read input file
file = open("day17.txt", 'r')

line = file.read()[:-1].split(':')[1].split(',')

# Calculates bounds of horizontal movement
x_bounds = tuple(map(int, line[0].strip().split('=')[1].split('..')))
print("x bounds:", x_bounds)

# Calculates bounds of vertical movement
y_bounds = tuple(map(int, line[1].strip().split('=')[1].split('..')))
print("y bounds:", y_bounds)

# Dictionary with starting velocity
velocity = {}

# Dictionary of trajectories with different starting speeds
trajectories = {}

# Tests different starting speeds and records values
for x in range(x_bounds[1]+1):
	for y in range(-abs(y_bounds[0]), abs(y_bounds[0])):
		velocity['x'] = x
		velocity['y'] = y
		trajectories[(x,y)] = trajectory(velocity, x_bounds, y_bounds)

print(max([max([y for x,y in lista]) for lista in trajectories.values()]))