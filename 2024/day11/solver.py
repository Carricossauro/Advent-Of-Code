import sys

from math import floor, log10

# memoization decorator for part 2
# stores cache based on the current iteration and stone
# not sure why i didn't just use functools.lru_cache
cache = {}
def use_cache(f):
    def wrapper(stone, iteration):
        if (stone, iteration) not in cache:
            cache[(stone, iteration)] = f(stone, iteration)
        return cache[(stone, iteration)]
    return wrapper

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        # parsing goes here
        self.stones = [int(x.strip()) for x in self.lines[0].split()]

    def part1(self):
        # i couldn't initially see how to solve this smartly
        # so i figured part 1 could probably be brute forced

        for _ in range(25):
            # for every blink (iteration), apply the stone transformation rules
            new_stones = []
            for stone in self.stones:
                if stone == 0:
                    # if 0, replace with 1
                    new_stones.append(1)
                else:
                    # otherwise, start by finding number of digits in stone
                    digits = floor(log10(stone)) + 1
                    if digits % 2 == 0:
                        # if even digits, split the stone in half
                        left = floor(stone / 10**(digits // 2))
                        rigth = stone - (left * 10**(digits // 2))

                        new_stones.append(left)
                        new_stones.append(rigth)
                    else:
                        # if odd digits, multiply by 2024
                        new_stones.append(stone * 2024)

            self.stones = new_stones
        
        return len(self.stones)

    def part2(self):
        # for part 2, brute force would never have worked
        # so i figured it had to be a memory based solution
        # applied some typical memoization and figured that would do the trick
        total = 0

        for stone in self.stones:
            total += stone_iteration(stone, 75)
        
        return total

@use_cache
def stone_iteration(stone, iteration):
    # iteration starts at 75, goes down to 0
    if iteration == 0:
        return 1
    
    if stone == 0:
        # if 0, replace with 1
        return stone_iteration(1, iteration - 1)
    else:
        # otherwise, start by finding number of digits in stone
        digits = floor(log10(stone)) + 1
        if digits % 2 == 0:
            # if even digits, split the stone in half
            left = floor(stone / 10**(digits // 2))
            rigth = stone - (left * 10**(digits // 2))

            return stone_iteration(left, iteration - 1) + stone_iteration(rigth, iteration - 1)
        else:
            # if odd digits, multiply by 2024
            return stone_iteration(stone * 2024, iteration - 1)
    
    
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