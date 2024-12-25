import sys

from itertools import product

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        # parsing goes here
        self.locks = []
        self.keys = []

        grids = [[]]
        for line in self.lines:
            if line == "\n":
                grids.append([])
            else:
                grids[-1].append(line.strip())

        self.N = len(grids[0])
        self.M = len(grids[0][0])
                
        for grid in grids:
            lock = (grid[0][0] == '#')

            if lock:
                self.locks.append([])
            else:
                self.keys.append([])

            for j in range(self.M):
                start = 0 if lock else self.N - 1
                limit = self.N if lock else -1
                step = 1 if lock else -1
                for i in range(start, limit, step):
                    if grid[i][j] == '.':
                        break
                
                if lock:
                    self.locks[-1].append(i - 1)
                else:
                    self.keys[-1].append(self.N - i - 2)

    def part1(self):
        total = 0

        key_space = self.N - 2
        for i, j in product(range(len(self.locks)), range(len(self.keys))):
            lock = self.locks[i]
            key = self.keys[j]

            valid = all(lock[i] + key[i] <= key_space for i in range(self.M))
            if valid:
                total += 1

        return total

    def part2(self):
        # solution goes here
        return None
    
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