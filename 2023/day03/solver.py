import sys

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        # get the number of rows and columns
        self.N = len(self.lines)
        self.M = len(self.lines[0].strip())

    def part1(self):
        total = 0
        for i, line in enumerate(self.lines):
            number = ''
            start = None # start position of number
            end = None # end position of number

            for j, char in enumerate(line):
                if char.isdigit():
                    # if the start position of the number has not been set, set it
                    if not number:
                        start = (i,j)

                    number += char
                elif number != '':
                    # set end position of number
                    end = (i,j-1)

                    adjacent_positions = self.get_adjacent_positions(start, end)
                    for x, y in adjacent_positions:
                        if self.lines[x][y] != '.' and not self.lines[x][y].isdigit():
                            total += int(number)
                            break

                    # clear variables for next number
                    number = ''
                    start = None
                    end = None
        
        return total

    def part2(self):
        total = 0

        # store the numbers' and the possible gears' positions
        data = {
            'numbers': [],
            '*': []
        }
        for i, line in enumerate(self.lines):
            number = ''
            start = None # start position of number
            end = None # end position of number

            for j, char in enumerate(line):
                if char == '*':
                    data['*'].append((i,j))
                if char.isdigit():
                    # if the start position of the number has not been set, set it
                    if not number:
                        start = (i,j)

                    number += char
                elif number != '':
                    # set end position of number
                    end = (i, j - 1)

                    data['numbers'].append((int(number), (start, end)))

                    # clear variables for next number
                    number = ''
                    start = None
                    end = None

        for possible_gear in data['*']:
            adjacent_numbers = []
            for number in data['numbers']:
                if self.is_adjacent(possible_gear, number[1]):
                    adjacent_numbers.append(number[0])

            if len(adjacent_numbers) == 2:
                total += adjacent_numbers[0] * adjacent_numbers[1]

        return total

    # function made by github copilot lol
    def get_adjacent_positions(self, start, end):
        adjacent_positions = []
        for i in range(start[0] - 1, end[0] + 2):
            for j in range(start[1] - 1, end[1] + 2):
                # check if the position is within the bounds of the grid
                if i >= 0 and i < self.N and j >= 0 and j < self.M:
                    # check if the position is not between the start and end positions
                    if not (i >= start[0] and i <= end[0] and j >= start[1] and j <= end[1]):
                        adjacent_positions.append((i,j))

        return adjacent_positions

    def is_adjacent(self, possible_gear, number):
        # check if the possible gear is adjacent to the number
        for i in range(number[0][0] - 1, number[1][0] + 2):
            for j in range(number[0][1] - 1, number[1][1] + 2):
                if (i,j) == possible_gear:
                    return True

        return False
    
if __name__ == '__main__':
    if len(sys.argv) > 1 and 1 <= int(sys.argv[1]) <= 2:
        if sys.argv[1] == '1':
            solver = Solver("input1.txt")
            print(solver.part1())
        else:
            solver = Solver("input1.txt")
            print(solver.part2())