from functools import reduce
from itertools import combinations
import sys

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        # parsing goes here
        self.boxes = []
        for line in self.lines:
            self.boxes.append(tuple(map(int, line.strip().split(','))))

    def dist(self, boxes):
        box1, box2 = boxes
        return ((box1[0] - box2[0]) ** 2 + (box1[1] - box2[1]) ** 2 + (box1[2] - box2[2]) ** 2) ** 0.5

    def part1(self):
        # combinations of boxes
        box_pairs = list(combinations(self.boxes, 2))
        box_pairs.sort(key=self.dist)
        
        # assign each box to a unique circuit
        circuits = {}
        for i, box in enumerate(self.boxes):
            circuits[box] = i

        circuits_counts = {i:1 for i in range(len(circuits))}
        # merge circuits based on proximity
        for box1, box2 in box_pairs[:1000]:
            target_circuit = circuits[box1]
            replace_circuit = circuits[box2]
            if target_circuit != replace_circuit:
                # if the two boxes belong to different circuits, merge them
                circuits_counts[target_circuit] += circuits_counts[replace_circuit]
                del circuits_counts[replace_circuit]
                
                for box in list(circuits.keys()):
                    if circuits[box] == replace_circuit:
                        circuits[box] = target_circuit

        # return product of three largest circuit lengths
        return reduce(lambda x, y: x * y, sorted(circuits_counts.values())[-3:])

    def part2(self):
        # combinations of boxes
        box_pairs = list(combinations(self.boxes, 2))
        box_pairs.sort(key=self.dist)
        
        # assign each box to a unique circuit
        circuits = {}
        for i, box in enumerate(self.boxes):
            circuits[box] = i
        n_circuits = len(circuits)

        # merge circuits based on proximity
        last_2_boxes = None
        for box1, box2 in box_pairs:
            target_circuit = circuits[box1]
            replace_circuit = circuits[box2]
            if target_circuit != replace_circuit:
                # if the two boxes belong to different circuits, merge them and decrease circuit count
                if n_circuits == 2:
                    # if only two remain, store the last two boxes' coordinates
                    last_2_boxes = (box1, box2)
                    break # this cut run time from 43s to 2s
                n_circuits -= 1
                for box in list(circuits.keys()):
                    if circuits[box] == replace_circuit:
                        circuits[box] = target_circuit

        # return product of X coordinate of the last two merged boxes
        return reduce(lambda x, y: x * y, map(lambda i: i[0], last_2_boxes))
    
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
            print("\nPart 1:", solver.part1())
        else:
            print("\nPart 2:", solver.part2())
    else:
        print("Usage: python3 solver.py [1 / 2] [test / test2 / 1 / 2]")
        print("Filenames: test.txt\n\t   test2.txt\n\t   input1.txt\n\t   input2.txt")