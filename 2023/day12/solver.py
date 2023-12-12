import sys
import re
from functools import lru_cache

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        self.rows = []
        for line in self.lines:
            split_line = line.split(" ")
            
            damaged_springs = list(map(int, split_line[1].split(",")))
            springs = split_line[0]

            self.rows.append({
                "damaged": damaged_springs,
                "springs": springs
            })

    # brute force solution
    # caching is crucial for this problem (part 2)
    @lru_cache(maxsize=None)
    def num_arrangements(self, line, damaged_springs):
        # line = ('.', '#', ..., "?")
        if line == ():
            # if line is over, check if all groups are covered
            return int(damaged_springs == ())
        
        N = len(line)
        if line[0] == '.':
            # spring not damaged, skip
            return self.num_arrangements(line[1:], damaged_springs)
        elif line[0] == '?':
            # try both options
            return self.num_arrangements(("#",) + line[1:], damaged_springs) + self.num_arrangements(line[1:], damaged_springs)
        elif line[0] == '#':
            if damaged_springs != ():
                number_of_damaged_springs = 0
                # check if there are enough damaged springs to get current group
                while number_of_damaged_springs < N and number_of_damaged_springs < damaged_springs[0] and line[number_of_damaged_springs] != '.':
                    number_of_damaged_springs += 1

                if number_of_damaged_springs == damaged_springs[0]:
                    # there are enough springs
                    if number_of_damaged_springs == N:
                        # if there are no more springs, check if it was the last one
                        return int(len(damaged_springs) == 1)
                    elif line[number_of_damaged_springs] in ['?', '.']:
                        # if there are more springs, check if the next one can be skipped
                        return self.num_arrangements(line[number_of_damaged_springs + 1:], damaged_springs[1:])
                
        return 0

    def part1(self):
        total = 0
        for row in self.rows:
            total_row = self.num_arrangements(tuple(row["springs"]), tuple(row["damaged"]))

            total += total_row

        return total

    def part2(self):
        # unfold lines
        for i, row in enumerate(self.rows):
            new_row = {}
            new_row["damaged"] = row["damaged"] * 5
            new_row["springs"] = "?".join([row["springs"]] * 5)

            self.rows[i] = new_row

        return self.part1()
    
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