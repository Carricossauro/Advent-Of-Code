import sys
from itertools import combinations, permutations

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        # parsing goes here
        self.antennas = {} # frequency: [positions]
        self.N = len(self.lines)
        self.M = len(self.lines[0].strip())

        for i, line in enumerate(self.lines):
            for j, cell in enumerate(line):
                if cell != '.':
                    if cell not in self.antennas:
                        self.antennas[cell] = []
                    self.antennas[cell].append((i, j))

    def part1(self):
        antinodes = set()

        for frequency in self.antennas:
            for a1, a2 in combinations(self.antennas[frequency], 2):
                x_1, y_1 = a1
                x_2, y_2 = a2

                x_dist = abs(x_1 - x_2)
                y_dist = abs(y_1 - y_2)

                pos_1 = (-1, -1)
                pos_2 = (-1, -1)
                
                # find the antinode positions
                if x_1 < x_2 and y_1 < y_2:
                    pos_1 = (x_1 - x_dist, y_1 - y_dist)
                    pos_2 = (x_2 + x_dist, y_2 + y_dist)
                elif x_1 < x_2 and y_1 > y_2:
                    pos_1 = (x_1 - x_dist, y_1 + y_dist)
                    pos_2 = (x_2 + x_dist, y_2 - y_dist)
                elif x_1 > x_2 and y_1 < y_2:
                    pos_1 = (x_1 + x_dist, y_1 - y_dist)
                    pos_2 = (x_2 - x_dist, y_2 + y_dist)
                elif x_1 > x_2 and y_1 > y_2:
                    pos_1 = (x_1 + x_dist, y_1 + y_dist)
                    pos_2 = (x_2 - x_dist, y_2 - y_dist)

                if 0 <= pos_1[0] < self.N and 0 <= pos_1[1] < self.M:
                    antinodes.add(pos_1)
                if 0 <= pos_2[0] < self.N and 0 <= pos_2[1] < self.M:
                    antinodes.add(pos_2)

        return len(antinodes)

    def part2(self):
        # i used permutations in this one because the math is simpler this way
        antinodes = set()

        for frequency in self.antennas:
            for a1, a2 in permutations(self.antennas[frequency], 2):
                x_1, y_1 = a1
                x_2, y_2 = a2

                x_dist = abs(x_1 - x_2)
                y_dist = abs(y_1 - y_2)

                i = 0
                pos_1 = a1
                while 0 <= pos_1[0] < self.N and 0 <= pos_1[1] < self.M:
                    antinodes.add(pos_1)

                    # move on to the next antinode
                    if x_1 < x_2 and y_1 < y_2:
                        pos_1 = (x_1 - i * x_dist, y_1 - i * y_dist)
                    elif x_1 < x_2 and y_1 > y_2:
                        pos_1 = (x_1 - i * x_dist, y_1 + i * y_dist)
                    elif x_1 > x_2 and y_1 < y_2:
                        pos_1 = (x_1 + i * x_dist, y_1 - i * y_dist)
                    elif x_1 > x_2 and y_1 > y_2:
                        pos_1 = (x_1 + i * x_dist, y_1 + i * y_dist)

                    i += 1

        return len(antinodes)
    
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