import sys

from itertools import permutations
from functools import lru_cache

A = 'A'
UP = '^'
DOWN = 'v'
LEFT = '<'
RIGHT = '>'

numerical_keypad = {'7': (0, 0), '8': (0, 1), '9': (0, 2),
                    '4': (1, 0), '5': (1, 1), '6': (1, 2),
                    '1': (2, 0), '2': (2, 1), '3': (2, 2),
                                 '0': (3, 1), 'A': (3, 2)}

directional_keypad = {              UP:   (0, 1), A:     (0, 2),
                      LEFT: (1, 0), DOWN: (1, 1), RIGHT: (1, 2)}

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        # parsing goes here
        self.codes = []

        for line in self.lines:
            code = line.strip()
            self.codes.append(code)

    def part1(self):
        # took me really long to figure this one out
        # recursive solution to calculate the cost of each code
        # since each keypad needs to return to A, we can calculate the cost of each button press individually
        # this applies to all nested keypads
        total = 0

        for code in self.codes:
            code_cost = self.calculate_code_cost(code, 2)

            total += code_cost * int(code[:-1])

        return total

    def part2(self):
        # this was the same as part 1, but with memoization
        total = 0

        for code in self.codes:
            code_cost = self.calculate_code_cost(code, 25)

            total += code_cost * int(code[:-1])

        return total
    
    def calculate_code_cost(self, code, levels):
        # this recursive function calculates the cost of each code
        # moves through buttons, finds the shortest path to the next button
        # calculates all the button presses for all the nested keypads
        # chooses the smallest cost (least button presses)

        # always starts at A
        position = numerical_keypad[A]
        shortest = 0
        for button in code:
            new_shortest = float('inf')

            # find the basic path to the next button
            # manhatan distance based path
            basic_path = self.basic_path(position, numerical_keypad[button])

            # find all permutations of the basic path
            for path in permutations(basic_path):
                if len(path) > 0:
                    # these are the edge cases for the numerical keypad
                    # specifically to avoid the bottom left edge
                    if position[0] == 3:
                        if position[1] == 1 and path[0] == LEFT:
                            continue
                        if position[1] == 2 and path[:2] == (LEFT, LEFT):
                            continue
                    elif position[1] == 0:
                        if position[0] == 2 and path[0] == DOWN:
                            continue
                        if position[0] == 1 and path[:2] == (DOWN, DOWN):
                            continue
                        if position[0] == 0 and path[:3] == (DOWN, DOWN, DOWN):
                            continue

                # if still here, the new path is valid

                # add the A button to the path
                path += (A,)

                # find the new cost of the path so far
                new_path_len = shortest + self.directional_keypad_paths(path, levels)

                new_shortest = min(new_shortest, new_path_len)
            
            # move to the next button and record the total cost so far
            position = numerical_keypad[button]
            shortest = new_shortest

        return shortest
    
    # part 2 required memoization
    @lru_cache(maxsize=None)
    def directional_keypad_paths(self, directions, level):
        # this recursive function calculates the cost of each movement in the previous keypad
        # moves through all previous button presses, finds the shortest path to the next button
        # based on the next keypads

        # if there are no more keypads, we have the cost of this path
        if level == 0:
            return len(directions)

        # always starts at A
        position = directional_keypad[A]
        shortest = 0
        for direction in directions:
            new_shortest = float('inf')

            # find the basic path to the next button
            # manhatan distance based path
            basic_path = self.basic_path(position, directional_keypad[direction])

            # find all permutations of the basic path
            for path in permutations(basic_path):
                if len(path) > 0:
                    # these are the edge cases for the directional keypad
                    # specifically to avoid the bottom left edge
                    if position[0] == 0:
                        if position[1] == 1 and path[0] == LEFT:
                            continue
                        if position[1] == 2 and path[:2] == (LEFT, LEFT):
                            continue
                    elif position[1] == 0:
                        if position[0] == 1 and path[0] == UP:
                            continue
                        if position[0] == 2 and path[:2] == (UP, UP):
                            continue
                        if position[0] == 3 and path[:3] == (UP, UP, UP):
                            continue

                # if still here, the new path is valid
                
                # add the A button to the path
                path += (A,)

                # find the new cost of the path so far
                new_path_len = shortest + self.directional_keypad_paths(path, level - 1)

                new_shortest = min(new_shortest, new_path_len)

            # move to the next button and record the total cost so far
            position = directional_keypad[direction]
            shortest = new_shortest
        
        return shortest
    
    @lru_cache(maxsize=None)
    def basic_path(self, start, end):
        # this function calculates the basic path between two points
        # based on the manhattan path between the two points
        directions = []

        if start[0] < end[0]:
            diff = end[0] - start[0]
            directions.extend([DOWN] * diff)
        elif start[0] > end[0]:
            diff = start[0] - end[0]
            directions.extend([UP] * diff)

        if start[1] < end[1]:
            diff = end[1] - start[1]
            directions.extend([RIGHT] * diff)
        elif start[1] > end[1]:
            diff = start[1] - end[1]
            directions.extend([LEFT] * diff)

        return directions
    
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