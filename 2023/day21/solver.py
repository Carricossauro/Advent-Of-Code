import sys
import numpy as np

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        self.garden = []
        for line in self.lines:
            self.garden.append(line.strip())

        self.X = len(self.garden)
        self.Y = len(self.garden[0])
        self.bounds = True

    # check if position is within bounds of garden
    def within_bounds(self, position):
        x, y = position

        # if bounds are disabled (part 2), return true
        return (not self.bounds) or (0 <= x < self.X and 0 <= y < self.Y)

    # check if position is not a rock
    def not_rock(self, position):
        x, y = position

        # if bounds are disabled (part 2), wrap around the garden
        return self.garden[x % self.X][y % self.Y] != '#' if not self.bounds else self.garden[x][y] != '#'

    # get all valid adjacent positions of a position
    def adjacent_positions(self, position):
        x, y = position
        possible_adjacent_positions = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

        # filter out invalid positions (out of bounds or rock)
        # don't filter out positions if bounds are disabled (part 2)
        return [p for p in possible_adjacent_positions if self.within_bounds(p) and self.not_rock(p)]

    # get all valid end positions for a given start position and a given number of steps
    # dynamic programming - probably would have worked with a BFS
    def possible_positions(self, start=(0, 0), K=64):
        self.positions = {}
        self.positions[0] = set([start])

        for k in range(1, K + 1):
            # get all positions possible after k - 1 steps
            previous_positions = self.positions[k - 1]
            self.positions[k] = set()

            for position in previous_positions:
                # get valid adjacent positions
                adjacent_positions = self.adjacent_positions(position)

                for adjacent_position in adjacent_positions:
                    # add adjacent position to the set of positions possible after k steps
                    self.positions[k].add(adjacent_position)

        return len(self.positions[K])
    
    # find the start position
    def find_start(self):
        for x in range(self.X):
            for y in range(self.Y):
                if self.garden[x][y] == 'S':
                    return (x, y)

    def part1(self):
        start = self.find_start()
        
        return self.possible_positions(start)

    # explanation of part 2:
    # https://youtu.be/xHIQ2zHVSjM?t=307
    def part2(self):
        self.bounds = False
        K = 65 + 131*2
        start = self.find_start()
        self.possible_positions(start, K)
        
        X, Y = [0, 1, 2], []
        for i in X:
            Y.append(len(self.positions[65 + 131 * i]))

        # quadratic fit formula from wolfram alpha
        # https://www.wolframalpha.com/input?i=quadratic+fit+calculator&assumption=%7B%22F%22%2C+%22QuadraticFitCalculator%22%2C+%22data3x%22%7D+-%3E%22%7B0%2C+1%2C+2%7D%22&assumption=%7B%22F%22%2C+%22QuadraticFitCalculator%22%2C+%22data3y%22%7D+-%3E%22%7B3784%2C+33680%2C+93366%7D%22

        model = np.polyfit(X, Y, 2)
        quadratic_fit = lambda x: int(np.ceil(model[2] + model[1] * x + model[0]*(x**2)))
        target = (26501365 - 65) // 131

        return quadratic_fit(target)
    
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