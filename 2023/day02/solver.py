from functools import reduce
import sys
import re

class Solver:
    limit = {
        'red': 12,
        'green': 13,
        'blue': 14,
    }

    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

    def part1(self):
        total = 0
        for line in self.lines:
            # get the game number
            game_number = int(re.search(r"Game (\d+)", line).group(1))
            
            # get the set of balls
            set = re.findall(r"(\d+ \w+)", line)
            possible = True
            for ballz in set:
                # get the number and color of the ball
                [number, color] = ballz.split(' ')
                if int(number) > self.limit[color]:
                    # if the number is greater than the limit, the game is not possible
                    possible = False
                    break

            if possible:
                # if the game is possible, add the game number to the total
                total += game_number

        return total

    def part2(self):
        total = 0
        for line in self.lines:
            minimum = {
                'red': 0,
                'green': 0,
                'blue': 0,
            }
            
            # get the set of balls
            set = re.findall(r"(\d+ \w+)", line)
            for ballz in set:
                # get the number and color of the ball
                [number, color] = ballz.split(' ')
                # update the minimum number of balls of each color
                minimum[color] = max(minimum[color], int(number))

            # add the product of the minimum number of balls of each color to the total
            total += reduce(lambda x, y: x * y, minimum.values())

        return total
    
if __name__ == '__main__':
    if len(sys.argv) > 1 and 1 <= int(sys.argv[1]) <= 2:
        if sys.argv[1] == '1':
            solver = Solver("input1.txt")
            print(solver.part1())
        else:
            solver = Solver("input1.txt")
            print(solver.part2())