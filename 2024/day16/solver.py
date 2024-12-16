import sys

OBSTACLE = '#'
START = 'S'
END = 'E'

DIRECTION_EAST = (0, 1)
DIRECTION_WEST = (0, -1)
DIRECTION_NORTH = (-1, 0)
DIRECTION_SOUTH = (1, 0)

directions = [DIRECTION_EAST, DIRECTION_SOUTH, DIRECTION_WEST, DIRECTION_NORTH]

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        # parsing goes here
        self.map = []
        self.end = None
        self.start = None
        self.N = len(self.lines)
        self.M = len(self.lines[0]) - 1

        for i, line in enumerate(self.lines):
            self.map.append([])
            for j, c in enumerate(line.strip()):
                if c == START:
                    self.start = (i, j)
                    self.map[i].append('.')
                elif c == 'E':
                    self.end = (i, j)
                    self.map[i].append(c)
                else:
                    self.map[i].append(c)

    def part1(self):
        # this was a bit of a tricky one
        # I had to use a 3D DP table to keep track of each cell's points for each direction
        # I used a queue to keep track of the cells that need to be visited
        # when a better path to a cell is found, I add it to the queue
        # then the next movements from that cell are (re)calculated
        self.cell_points = {((i, j), direction) : float("inf") for i in range(self.N) for j in range(self.M) for direction in directions}
        self.cell_points[(self.start, DIRECTION_EAST)] = 0

        queue = [(self.start, DIRECTION_EAST)]
        for (x, y), direction in queue:
            for new_direction in directions:
                dx, dy = new_direction
                new_x, new_y = x + dx, y + dy

                if (dx, dy) == direction:
                    new_points = self.cell_points[((x, y), direction)] + 1
                elif (-dx, -dy) == direction:
                    new_points = self.cell_points[((x, y), direction)] + 2001
                else:
                    new_points = self.cell_points[((x, y), direction)] + 1001

                if self.map[new_x][new_y] != OBSTACLE and new_points < self.cell_points[((new_x, new_y), new_direction)]:
                    self.cell_points[((new_x, new_y), new_direction)] = new_points
                    if (new_x, new_y) != self.end:
                        queue.append(((new_x, new_y), new_direction))

        return min(self.cell_points[(self.end, direction)] for direction in directions)

    def part2(self):
        # first run part 1 to find the points for each cell
        # then i will get a table with the points of each cell for each direction
        # work backwards from the end to the start
        # i though this would run not much faster than part 1, I was wrong, it's very slow
        final_points = self.part1()

        spots = set()

        queue = [(self.end, direction) for direction in directions if self.cell_points[(self.end, direction)] == final_points]
        for ((x, y), direction) in queue:
            spots.add((x, y))

            # consider all 4 neighbors, each with all 4 directions
            neighbors = [((x - dx, y - dy), old_direction) for dx, dy in directions for old_direction in directions if (x - dx, y - dy) != (x, y)]
            for (old_x, old_y), old_direction in neighbors:
                # calculate the points difference for this cell and direction combo
                if old_direction == direction:
                    point_diff = self.cell_points[((x, y), direction)] - 1
                elif (-old_direction[0], -old_direction[1]) == direction:
                    point_diff = self.cell_points[((x, y), direction)] - 2001
                else:
                    point_diff = self.cell_points[((x, y), direction)] - 1001
                
                # add any of the previous cells if they have the correct amount of points
                if (0 <= old_x < self.N and 0 <= old_y < self.M and self.cell_points[((old_x, old_y), old_direction)] == point_diff):
                    queue.append(((old_x, old_y), old_direction))

        return len(spots)
    
if __name__ == '__main__':
    if len(sys.argv) > 2 and 1 <= int(sys.argv[1]) <= 2:

        if sys.argv[2] == 'test':
            solver = Solver("test.txt")
        elif sys.argv[2] == 'test2':
            solver = Solver("test2.txt")
        elif sys.argv[2] == '1':
            solver = Solver("input1.txt")
        elif sys.argv[2] == '2':
            solver = Solver("input2.txt")

        if sys.argv[1] == '1':
            print(solver.part1())
        else:
            print(solver.part2())
    else:
        print("Usage: python3 solver.py [1 / 2] [test / test2 / 1 / 2]")
        print("Filenames: test.txt\n\t   test2.txt\n\t   input1.txt\n\t   input2.txt")