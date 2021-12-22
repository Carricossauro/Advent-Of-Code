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

def within_boundaries(trajectory, x_bounds, y_bounds):
	return any( [x_bounds[0] <= x <= x_bounds[1] and y_bounds[0] <= y <= y_bounds[1] for x,y in trajectory] )

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

# Set of distinct starting speed values that reach the target area after any step
values = set()

# Tests different starting speeds and records values
# The bounds in the range() for y are probably exagerated but it's the only way I knew it would work
for x in range(x_bounds[1]+1):
	for y in range(-abs(y_bounds[0]), abs(y_bounds[0])):
		velocity['x'] = x
		velocity['y'] = y
		trajectories[(x,y)] = trajectory(velocity, x_bounds, y_bounds)
		if within_boundaries(trajectories[(x,y)], x_bounds, y_bounds):
			values.add((x,y))

print(len(values))