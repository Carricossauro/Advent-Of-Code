import sys
import re
import numpy as np
from functools import reduce

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        # first line contains instructions
        self.instructions = self.lines[0].strip()

        self.nodes = {}
        for line in self.lines[1:]:
            positions = re.findall(r"(\w+)", line) # current_node = (left_node, right_node)
            if len(positions) == 3:
                current = positions[0] # current node
                left = positions[1] # left node
                right = positions[2] # right node

                # add to nodes
                self.nodes[current] = (left, right)

    def calculate_steps(self, current_node, end_node = None):
        total = 0

        # loop until end node is reached
        while (end_node and current_node != end_node) or (not end_node and current_node[-1] != 'Z'):
            # get instruction
            instruction = self.instructions[total % len(self.instructions)]

            # update node
            if instruction == 'L':
                current_node = self.nodes[current_node][0]
            else:
                current_node = self.nodes[current_node][1]

            total += 1

        return total

    def part1(self):
        return self.calculate_steps('AAA', end_node='ZZZ')

    def part2(self):
        current_nodes = list(filter(lambda x: x[-1] == 'A', self.nodes.keys())) # get all nodes that end with A
        steps = list(map(self.calculate_steps, current_nodes)) # find number steps for each node
        
        # find lowest common multiple of all steps
        return reduce(np.lcm, steps)
                    
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