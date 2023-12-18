import sys
import bisect

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
DIRECTIONS = [UP, RIGHT, DOWN, LEFT]

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        self.lavafall = []
        for line in self.lines:
            self.lavafall.append(list(map(int, line.strip())))

        self.X = len(self.lavafall)
        self.Y = len(self.lavafall[0])

    def next_positions(self, x, y, direction, next_direction, minimum_moves=1, maximum_moves=3):
        positions = []

        moves = maximum_moves
        move = 1
        
        # start with heat loss of current position
        heat_loss = self.heat_loss[((x, y), direction)]
        while move <= moves:
            # get coordinates of next position
            if next_direction == UP:
                nx, ny = x - move, y
            elif next_direction == DOWN:
                nx, ny = x + move, y
            elif next_direction == LEFT:
                nx, ny = x, y - move
            elif next_direction == RIGHT:
                nx, ny = x, y + move

            # check if next position is in grid
            if 0 <= nx < self.X and 0 <= ny < self.Y:
                heat_loss += self.lavafall[nx][ny] # add heat loss of passed position
                if move >= minimum_moves:
                    positions.append(((nx, ny), heat_loss))
            else:
                # if next position is not in grid, the others won't be either
                break

            move += 1

        return positions

    def find_shortest_path(self, start=[((0, 0), RIGHT), ((0, 0), DOWN)], end=None, minimum_moves=1, maximum_moves=3):
        if end is None:
            end = (self.X - 1, self.Y - 1)

        queue = start
        self.heat_loss = {((x, y), next_direction):float("inf") for x in range(self.X) for y in range(self.Y) for next_direction in DIRECTIONS for consecutive_moves in range(4)}
        self.previous = {}

        for element  in start:
            self.heat_loss[element] = 0
            self.previous[element] = None

        # dijkstra's algorithm
        while queue:
            # get position/direction combination with lowest heat loss
            i = min(range(len(queue)), key=lambda i: self.heat_loss[queue[i]])
            (x, y), direction = queue.pop(i)

            if (x, y) == end:
                return self.heat_loss[((x, y), direction)]

            # rotate left or right
            for next_direction in [(direction + 1) % 4, (direction - 1) % 4]:
                for (nx, ny), heat_loss in self.next_positions(x, y, direction, next_direction, minimum_moves, maximum_moves):
                    # update and recalculate values if found a faster path to a position
                    if ((nx, ny), next_direction) not in self.heat_loss or heat_loss < self.heat_loss[((nx, ny), next_direction)]:
                        self.heat_loss[((nx, ny), next_direction)] = heat_loss
                        self.previous[((nx, ny), next_direction)] = ((x, y), direction)
                        queue.append(((nx, ny), next_direction))

    def part1(self):
        heat_loss = self.find_shortest_path()

        return heat_loss

    def part2(self):
        heat_loss = self.find_shortest_path(minimum_moves=4, maximum_moves=10)

        return heat_loss
    
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