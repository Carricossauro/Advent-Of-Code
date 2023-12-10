import sys

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        self.pipes = []
        for line in self.lines:
            self.pipes.append(list(line.strip()))

        self.X = len(self.pipes) # number of rows
        self.Y = len(self.pipes[0]) # number of columns

    # find the starting point
    def find_start(self):
        for i, row in enumerate(self.pipes):
            for j, char in enumerate(row):
                if char == 'S':
                    self.start = (i, j)

    # find all adjacent pipes      
    def adjacent(self, x, y):
        # all possible combinations of pipes at the next position
        combinations = {
            (x - 1, y): ['|', 'F', '7', 'S'], # up
            (x + 1, y): ['|', 'L', 'J', 'S'], # down
            (x, y - 1): ['-', 'F', 'L', 'S'], # left
            (x, y + 1): ['-', '7', 'J', 'S'], # right
        }
        possible = []
        
        if self.pipes[x][y] == '|':
            possible = [(x - 1, y), (x + 1, y)] # up, down
        elif self.pipes[x][y] == '-':
            possible = [(x, y - 1), (x, y + 1)] # left, right
        elif self.pipes[x][y] == '7':
            possible = [(x, y - 1), (x + 1, y)] # left, down
        elif self.pipes[x][y] == 'J':
            possible = [(x, y - 1), (x - 1, y)] # left, up
        elif self.pipes[x][y] == 'L':
            possible = [(x, y + 1), (x - 1, y)] # right, up
        elif self.pipes[x][y] == 'F':
            possible = [(x, y + 1), (x + 1, y)] # right, down
        elif self.pipes[x][y] == 'S':
            # add all surrounding pipes
            possible = [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)] # up, down, left, right

        # filter out invalid coordinates and non-pipes
        return list(filter(lambda x: 0 <= x[0] < self.X and 0 <= x[1] < self.Y and self.pipes[x[0]][x[1]] in combinations[x], possible))

    # find the distance from the starting point to all other points
    # find_start() must be called first
    def calculate_distances(self):
        self.distances = {}
        start_x, start_y = self.start

        # BFS
        queue = [(start_x, start_y, 0)] # (x, y, distance)
        for x, y, distance in queue:
            self.distances[(x, y)] = distance

            next_positions = self.adjacent(x, y)
            for next_x, next_y in next_positions:
                if (next_x, next_y) not in self.distances or self.distances[(next_x, next_y)] > distance + 1:
                    # add to queue if not visited or if the new distance is shorter
                    queue.append((next_x, next_y, distance + 1))

    def part1(self):
        self.find_start()

        self.calculate_distances()

        # find the longest distance
        return max(self.distances.values())

    def part2(self):
        self.find_start()

        self.calculate_distances()
        
        self.inside = 0
        for i in range(self.X):
            insideLoop = False # flip this variable when we enter or exit the loop inner area
            for j in range(self.Y):
                if (i, j) in self.distances:
                    if self.pipes[i][j] in ['L', 'J', '|']:
                        insideLoop = not insideLoop
                elif insideLoop:
                    self.inside += 1

        return self.inside
    
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