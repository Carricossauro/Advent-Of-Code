import sys

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

# dx and dy are used to move in the grid
# mitigates human error when writing the code for each direction change
dx = {UP: -1, RIGHT: 0, DOWN: 1, LEFT: 0 }
dy = {UP: 0 , RIGHT: 1, DOWN: 0, LEFT: -1}

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        self.grid = []
        for line in self.lines:
            self.grid.append(list(line.strip()))

        self.X = len(self.grid)
        self.Y = len(self.grid[0])

    # go through the grid with all active beams and find all energized cells
    def find_energized_beams(self, start=(0, 0, RIGHT)):
        self.energized = set()
        self.beams = [start]
        self.visited = set()

        # this is essentially a BFS
        while self.beams:
            new_beams = []

            for beam in self.beams:
                # check if beam is in grid and not visited
                if beam not in self.visited and 0 <= beam[0] < self.X and 0 <= beam[1] < self.Y:
                    x, y, direction = beam

                    self.energized.add((x, y))
                    self.visited.add(beam)
                    
                    if self.grid[x][y] == '|':
                        if direction == UP or direction == DOWN:
                            # if beam is going up or down, it will continue in the same direction
                            new_direction = direction
                        else:
                            # if beam is going left or right, it will split into two beams
                            new_direction = None
                            self.beams.append((x + dx[UP], y + dy[UP], UP))
                            self.beams.append((x + dx[DOWN], y + dy[DOWN], DOWN))
                    elif self.grid[x][y] == '-':
                        if direction == LEFT or direction == RIGHT:
                            # if beam is going left or right, it will continue in the same direction
                            new_direction = direction
                        else:
                            # if beam is going up or down, it will split into two beams
                            new_direction = None
                            self.beams.append((x + dx[LEFT], y + dy[LEFT], LEFT))
                            self.beams.append((x + dx[RIGHT], y + dy[RIGHT], RIGHT))
                    elif self.grid[x][y] == '/':
                        if direction == UP:
                            # if beam is going up, it will continue to the right
                            new_direction = RIGHT
                        elif direction == RIGHT:
                            # if beam is going right, it will continue up
                            new_direction = UP
                        elif direction == DOWN:
                            # if beam is going down, it will continue to the left
                            new_direction = LEFT
                        else:
                            # if beam is going left, it will continue down
                            new_direction = DOWN
                    elif self.grid[x][y] == '\\':
                        if direction == UP:
                            # if beam is going up, it will continue to the left
                            new_direction = LEFT
                        elif direction == RIGHT:
                            # if beam is going right, it will continue down
                            new_direction = DOWN
                        elif direction == DOWN:
                            # if beam is going down, it will continue to the right
                            new_direction = RIGHT
                        else:
                            # if beam is going left, it will continue up
                            new_direction = UP
                    else:
                        # if there is no mirror, beam will continue in the same direction
                        new_direction = direction

                    if new_direction is not None:
                        # if direction changed, update beam coordinates and direction
                        # in case of splits, new beams have already been handled
                        new_beams.append((x + dx[new_direction], y + dy[new_direction], new_direction))

            self.beams = new_beams

    def part1(self):
        self.find_energized_beams()

        return len(self.energized)

    def part2(self):
        # this part takes a bit more to run
        # ~2.5 sec on my machine for my input
        self.energized_configurations = []
        start = []

        # find all beams that start on the edge of the grid
        for i in range(self.X):
            for j in range(self.Y):
                if i == 0:
                    start.append((i, j, DOWN))
                elif i == self.X - 1:
                    start.append((i, j, UP))

                if j == 0:
                    start.append((i, j, RIGHT))
                elif j == self.Y - 1:
                    start.append((i, j, LEFT))

        for start_beam in start:
            self.find_energized_beams(start_beam)
            self.energized_configurations.append(len(self.energized))

        return max(self.energized_configurations)
    
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