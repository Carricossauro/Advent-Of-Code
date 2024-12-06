import sys

OBSTACLE = '#'
OPEN = '.'
CROSSED = 'X'

GUARD_FACING_UP = '^'
GUARD_FACING_DOWN = 'v'
GUARD_FACING_LEFT = '<'
GUARD_FACING_RIGHT = '>'

GUARD_DIRECTION_UP = (-1, 0)
GUARD_DIRECTION_DOWN = (1, 0)
GUARD_DIRECTION_LEFT = (0, -1)
GUARD_DIRECTION_RIGHT = (0, 1)

map_guard_direction = {GUARD_FACING_UP: GUARD_DIRECTION_UP,
                       GUARD_FACING_DOWN: GUARD_DIRECTION_DOWN,
                       GUARD_FACING_LEFT: GUARD_DIRECTION_LEFT,
                       GUARD_FACING_RIGHT: GUARD_DIRECTION_RIGHT}

map_guard_rotation = {GUARD_DIRECTION_UP: GUARD_DIRECTION_RIGHT,
                      GUARD_DIRECTION_RIGHT: GUARD_DIRECTION_DOWN,
                      GUARD_DIRECTION_DOWN: GUARD_DIRECTION_LEFT,
                      GUARD_DIRECTION_LEFT: GUARD_DIRECTION_UP}

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        # parsing goes here
        self.grid = []
        self.guard = None
        self.N = len(self.lines)
        self.M = len(self.lines[0]) - 1

        i = 0
        for line in self.lines:
            self.grid.append([])
            j = 0
            for c in line:
                if c == '\n':
                    continue
                self.grid[i].append((c, set()))
                if c in map_guard_direction:
                    self.guard = ((i, j), map_guard_direction[c])
                    self.grid[i][j] = (OPEN, set())
                j += 1
            i += 1

    def part1(self):
        # this is a pretty simple map traversal, we already know how the guard will move
        # this worked on the first try, was not that complicated
        total_crossed = 0
        guard = self.guard

        moving = True
        while moving:
            # find guard's position and direction
            x, y , dir = guard[0][0], guard[0][1], guard[1]

            current_cell = self.grid[x][y]
            # check if the cell has been crossed in this direction (avoid loops)
            if current_cell[0] == CROSSED and dir in current_cell[1]:
                moving = False
                continue
            # add direction to cell
            current_cell[1].add(dir)
            self.grid[x][y] = (CROSSED, current_cell[1])
            # count crossed cells
            total_crossed += (current_cell[0] == OPEN)

            # move guard
            next_x, next_y = x + dir[0], y + dir[1]
            if next_x < 0 or next_x >= self.N or next_y < 0 or next_y >= self.M:
                # if out of bounds, stop
                moving = False
            else:
                # if next cell is an obstacle, rotate
                next_cell = self.grid[next_x][next_y]
                if next_cell[0] == OBSTACLE:
                    dir = map_guard_rotation[dir]
                    next_x, next_y = x + dir[0], y + dir[1]
                guard = ((next_x, next_y), dir)

        return total_crossed

    def part2(self):
        # run the first part to find the path that the guard takes
        # use the crossed positions to add obstacles to the grid
        # brute force the guard's path for each new obstacle to look for loops
        self.part1()
        total_loops = 0

        for i in range(self.N):
            for j in range(self.M):
                # if cell is not originally crossed, skip
                if self.grid[i][j][0] != CROSSED:
                    continue

                # create new guard and grid objects to keep the original ones
                guard = self.guard
                new_grid = []
                for ii, line in enumerate(self.grid):
                    new_grid.append([])
                    for jj, cell in enumerate(line):
                        if cell[0] == CROSSED:
                            if i == ii and j == jj:
                                # add obstacle to the new grid
                                new_grid[-1].append((OBSTACLE, set()))
                            else:
                                # remove crossed status from the cell
                                new_grid[-1].append((OPEN, set()))
                        else:
                            # copy non-crossed cell to new grid
                            new_grid[-1].append((cell[0], set()))

                moving = True
                loop = False
                while moving:
                    # find guard's position and direction
                    x, y , dir = guard[0][0], guard[0][1], guard[1]

                    current_cell = new_grid[x][y]
                    # check if the cell has been crossed in this direction (find loops)
                    if current_cell[0] == CROSSED and dir in current_cell[1]:
                        moving = False
                        loop = True
                        break 
                    # add direction to cell
                    current_cell[1].add(dir)
                    new_grid[x][y] = (CROSSED, current_cell[1])

                    # move guard
                    next_x, next_y = x + dir[0], y + dir[1]
                    if next_x < 0 or next_x >= self.N or next_y < 0 or next_y >= self.M:
                        # if out of bounds, stop
                        moving = False
                    else:
                        # if next cell is an obstacle, rotate
                        next_cell = new_grid[next_x][next_y]
                        # this part was why i took too long
                        # i forgot to check if the next cell after rotation was an obstacle
                        # if it is, need to rotate again
                        # this will never be an infinite loop because the guard comes from a non-obstacle cell (so there is at least one)
                        # there is only a few cases where this would fail, if the guard is initially surrounded by 3 obstacles
                        # eg.  #
                        #     #v#
                        # in this case, we would eventually place an obstacle in front of them and force them to rotate endlessly
                        # but this case is not in the input
                        while next_cell[0] == OBSTACLE:
                            dir = map_guard_rotation[dir]
                            next_x, next_y = x + dir[0], y + dir[1]
                            if next_x < 0 or next_x >= self.N or next_y < 0 or next_y >= self.M:
                                # if out of bounds, stop
                                moving = False
                                break
                            next_cell = new_grid[next_x][next_y]
                        guard = ((next_x, next_y), dir)

                if loop:
                    total_loops += 1
                
        return total_loops
    
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