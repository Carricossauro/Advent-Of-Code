import sys

from functools import lru_cache

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        # parsing goes here
        self.towels = set()
        self.designs = []

        for i, line in enumerate(self.lines):
            if i == 0:
                self.towels = set(map(lambda x: x.strip(), line.split(',')))
            elif i >= 2:
                self.designs.append(line.strip())

    def part1(self):
        # i wasted so much time trying to create a DP algorithm for this
        # but it was just a basic recursive problem with caching
        total = 0

        for design in self.designs:
            total += self.is_design_possible(design)

        return total

    def part2(self):
        # not much changed
        # just counts all possible designs instead of just finding the first
        total = 0

        for design in self.designs:
            total += self.count_possible_designs(design)

        return total
    
    @lru_cache
    def is_design_possible(self, design):
        if design == '':
            return True
        
        for towel in self.towels:
            if design.startswith(towel):
                if self.is_design_possible(design[len(towel):]):
                    return True
        
        return False
    
    @lru_cache
    def count_possible_designs(self, design):
        if design == '':
            return 1
        
        total = 0
        for towel in self.towels:
            if design.startswith(towel):
                total += self.count_possible_designs(design[len(towel):])
        
        return total
        
    
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