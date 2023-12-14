import sys

# this order is important
# it is used to iterate through
# the tilts in the correct order
NORTH = 0
WEST = 1
SOUTH = 2
EAST = 3

move = {
    NORTH: (-1, 0),
    WEST: (0, -1),
    SOUTH: (1, 0),
    EAST: (0, 1)
}

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        # parsing goes here
        self.initial = [] # save initial board for part 2
        self.rocks = []
        for line in self.lines:
            self.rocks.append(list(line.strip()))
            self.initial.append(list(line.strip()))

        self.X = len(self.rocks[0]) 
        self.Y = len(self.rocks)

        self.previous = []
    
    # push the rock in the given direction
    def push(self, direction, start_x, start_y):
        dx, dy = move[direction]
        x, y = start_x + dx, start_y + dy

        # move the rock until it hits a wall or another rock
        while 0 <= x < self.X and 0 <= y < self.Y and self.rocks[x][y] == '.':
            x += dx
            y += dy

        new_x, new_y = x - dx, y - dy
        # if the rock is not at the starting position, move its place
        if (new_x, new_y) != (start_x, start_y):
            self.rocks[new_x][new_y] = 'O'
            self.rocks[start_x][start_y] = '.'
        
    # tilt the board in the given direction
    def tilt(self, direction):
        # we need to iterate through the rocks in the correct order
        # so that the rocks are pushed in the correct order
        # (the moved rocks will get in the way of the other rocks)
        if direction == NORTH:
            # move left to right, top to bottom
            for x in range(self.X):
                for y in range(self.Y):
                    if self.rocks[x][y] == 'O':
                        # push the rock in the given direction
                        self.push(direction, x, y)
        elif direction == WEST:
            # move top to bottom, left to right
            for y in range(self.Y):
                for x in range(self.X):
                    if self.rocks[x][y] == 'O':
                        # push the rock in the given direction
                        self.push(direction, x, y)
        elif direction == SOUTH:
            # move right to left, bottom to top
            # this could have been simpler, but I let copilot do its thing
            # y did not need to be reversed
            for x in range(self.X - 1, -1, -1):
                for y in range(self.Y - 1, -1, -1):
                    if self.rocks[x][y] == 'O':
                        # push the rock in the given direction
                        self.push(direction, x, y)
        elif direction == EAST:
            # move bottom to top, right to left
            # this could also have been simpler, but I let copilot do its thing
            # x did not need to be reversed
            for y in range(self.Y - 1, -1, -1):
                for x in range(self.X - 1, -1, -1):
                    if self.rocks[x][y] == 'O':
                        # push the rock in the given direction
                        self.push(direction, x, y)

    def part1(self):
        self.tilt(NORTH)

        return sum([rocks.count('O') * (self.X - i) for i, rocks in enumerate(self.rocks)])

    # perform 1 cycle, tilt the board in all directions
    def cycle(self):
        # tilt the board in all directions
        for direction in range(4):
            self.tilt(direction)

    # check if the current board is the same as a previous board
    def is_loop(self, rocks):
        for i in range(len(self.previous)):
            if rocks == self.previous[i]:
                return i
            
        return False
    
    # find the rocks on the board
    def find_rocks(self):
        rocks = []
        for x in range(self.X):
            for y in range(self.Y):
                if self.rocks[x][y] == 'O':
                    rocks.append((x, y))
        
        return rocks

    def part2(self):
        cycles = 1000000000

        for i in range(cycles):
            self.cycle()

            if j := self.is_loop(self.find_rocks()):
                loop_length = i - j
                # new cycle amount = cycles until start of the loop + total cycles % loop length
                new_cycles = j + (cycles - j) % (loop_length)
                break
            else:
                self.previous.append(self.find_rocks())

        self.rocks = self.initial
        for i in range(new_cycles):
            self.cycle()

        return sum([rocks.count('O') * (self.X - i) for i, rocks in enumerate(self.rocks)])
    
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