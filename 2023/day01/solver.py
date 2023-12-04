import sys
import re

class Solver:
    digits = {
        "one": 1, "two": 2, "three": 3,
        "four": 4, "five": 5, "six": 6,
        "seven": 7, "eight": 8, "nine": 9}
    
    expression = "(?=(one|two|three|four|five|six|seven|eight|nine|\d))"
    
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

    def part1(self):
        total = 0
        for line in self.lines:
            first = None
            last = None
            for character in line:
                if character.isdigit():
                    if first is None:
                        first = int(character)
                    last = int(character)

            total += (first*10)+last

        return total

    def part2(self):
        total = 0
        for line in self.lines:
            found_digits = [int(character) if character.isdigit() else self.digits[character] for character in re.findall(self.expression, line)]

            total += (found_digits[0] * 10) +  found_digits[-1]

        return total
    
if __name__ == '__main__':
    if len(sys.argv) > 1 and 1 <= int(sys.argv[1]) <= 2:
        if sys.argv[1] == '1':
            solver = Solver("input1.txt")
            print(solver.part1())
        else:
            solver = Solver("input1.txt")
            print(solver.part2())