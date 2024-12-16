import sys

map_direction = {
    '<': (0, -1),
    '>': (0, 1),
    '^': (-1, 0),
    'v': (1, 0)
}

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        # parsing goes here
        self.warehouse = []
        self.moves = []
        self.robot = None

        reading_map = True
        for i, line in enumerate(self.lines):
            if line == '\n':
                reading_map = False
                continue

            if reading_map:
                self.warehouse.append([])
                for j, cell in enumerate(line.strip()):
                    if cell == "@":
                        self.robot = (i, j)
                        self.warehouse[-1].append(".")
                    else:
                        self.warehouse[-1].append(cell)
            else:
                self.moves += list(line.strip())

        self.N = len(self.warehouse)
        self.M = len(self.warehouse[0])

    def part1(self):
        total = 0

        for move in self.moves:
            dx, dy = map_direction[move]

            x, y = self.robot

            # iterate boxes until we find a free space or a wall
            while 0 < x < self.N - 1 and 0 < y < self.M - 1 and self.warehouse[x + dx][y + dy] == 'O':
                x += dx
                y += dy

            # if we found a free space, move the boxes
            if self.warehouse[x + dx][y + dy] == '.':
                # move every box until we find the robot again
                while (x, y) != self.robot:
                    self.warehouse[x + dx][y + dy] = 'O'
                    x -= dx
                    y -= dy

                # move the robot
                self.warehouse[self.robot[0]][self.robot[1]] = '.'
                self.robot = (self.robot[0] + dx, self.robot[1] + dy)
                self.warehouse[self.robot[0]][self.robot[1]] = '@'

        for i, row in enumerate(self.warehouse):
            for j, cell in enumerate(row):
                if cell == 'O':
                    total += 100 * i + j

        return total

    def part2(self):
        # start by expanding the map
        # then use the same logic as part 1, but considering a set of positions affected by the move (since each box is 2 cells)
        # for each position, considers what other position that affects
        # then sort the positions by the order they should be moved (from the farthest to the closest to the robot)
        self.expand_map()

        total = 0

        for move in self.moves:
            will_move = True
            dx, dy = map_direction[move]

            x, y = self.robot

            positions_affected = set([])
            queue = [(x, y, '@')]
            for x, y, symbol in queue:
                positions_affected.add((x, y, symbol))

                new_x, new_y = x + dx, y + dy
                if self.warehouse[new_x][new_y] == '#':
                    # if we hit a wall, nothing can move
                    will_move = False
                elif self.warehouse[new_x][new_y] != '.':
                    # if we hit a box, we need to move it
                    # determine the left and right position of the box based on the one we found
                    if self.warehouse[new_x][new_y] == '[':
                        left_x, left_y = new_x, new_y
                        right_x, right_y = new_x, new_y + 1
                    else:
                        left_x, left_y = new_x, new_y - 1
                        right_x, right_y = new_x, new_y

                    # add the left and right positions to the queue, without repetition
                    if (left_x, left_y, '[') not in positions_affected:
                        queue.append((left_x, left_y, '['))

                    if (right_x, right_y, ']') not in positions_affected:
                        queue.append((right_x, right_y, ']'))

            if will_move:
                # if no walls were hit, we can move the boxes and robot
                # sort the positions by the order they should be moved
                # from the farthest to the closest to the robot
                positions_affected = sorted(list(positions_affected), key=lambda x: x[0] * dx + x[1] * dy, reverse=True)
                for x, y, cell in positions_affected:
                    self.warehouse[x][y] = "."
                    self.warehouse[x + dx][y + dy] = cell

                self.robot = (self.robot[0] + dx, self.robot[1] + dy)

        for i, row in enumerate(self.warehouse):
            for j, cell in enumerate(row):
                if cell == '[':
                    total += 100 * i + j

        return total
    
    def expand_map(self):
        # this part doesn't really need much explaining
        # it's just a direct code translation of the description
        new_warehouse = []

        for i in range(self.N):
            new_warehouse.append([])
            for j in range(self.M):
                if self.warehouse[i][j] == '#':
                    new_warehouse[-1].append('#')
                    new_warehouse[-1].append('#')
                elif self.warehouse[i][j] == 'O':
                    new_warehouse[-1].append('[')
                    new_warehouse[-1].append(']')
                elif (i, j) == self.robot:
                    new_robot = (i, 2 * j)
                    new_warehouse[-1].append('@')
                    new_warehouse[-1].append('.')
                else:
                    new_warehouse[-1].append('.')
                    new_warehouse[-1].append('.')

        self.robot = new_robot
        self.warehouse = new_warehouse
        self.N *= 2
        self.M *= 2
    
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