import sys

import networkx as nx
import matplotlib.pyplot as plt

apply_gate = {
    'AND': lambda x, y: int(x + y == 2),
    'OR': lambda x, y: int(x + y >= 1),
    'XOR': lambda x, y: int(x + y == 1)
}

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        # parsing goes here
        self.bits = {}
        self.gate_types = {}
        self.gates = nx.DiGraph()

        reading_bits = True
        for line in self.lines:
            if line == '\n':
                reading_bits = False
                continue

            if reading_bits:
                line = line.strip().split(':')
                self.bits[line[0]] = int(line[1].strip())
                self.gate_types[line[0]] = ''
            else:
                line = line.strip().split(' -> ')
                input1, gate, input2 = line[0].split(' ')
                output = line[1]
                
                self.gates.add_edge(input1, output)
                self.gates.add_edge(input2, output)
                self.gate_types[output] = gate

    def part1(self, binary=False):
        # pretty simple part 1

        # start with the outputs of the gates from bits that are already known
        queue = [item for sublist in [list(self.gates.successors(x)) for x in self.bits.keys()] for item in sublist]
        self.apply_gates(queue)

        binary_result = ''.join(map(lambda x: str(self.bits[x]), sorted([x for x in self.bits if x.startswith('z')], reverse=True)))

        return binary_result if binary else int(binary_result, 2)

    def part2(self):
        # it's done but I still don't really get it
        # this could just be solved by analyzing the graph and seeing what didn't fit (hence the self.stats)
        # but I'm not sure why some of there rules are here (line 62 and the second part of line 75)
        # i got those rules from reddit
        wrong = set()
        self.stats = {}
        for node in self.gates.nodes():
            inputs = list(self.gates.predecessors(node))
            gate = self.gate_types[node]

            if (node.startswith('z') and gate != 'XOR' and node != 'z45') or (gate =="XOR" and node[0] not in ['x', 'y', 'z'] and all(x[0] not in ['x', 'y', 'z'] for x in inputs)):
                wrong.add(node)

            for input in inputs:
                input_gate = self.gate_types[input]

                x = (input_gate, gate)
                if x not in self.stats:
                    self.stats[x] = 0
                self.stats[x] += 1

                previous_gate_inputs = list(self.gates.predecessors(input))

                if x in [('XOR', 'OR'), ('AND', 'AND'), ('AND', 'XOR')] and 'x00' not in previous_gate_inputs:
                    wrong.add(input)

        return self.stats, ",".join(sorted(wrong))
    
    def apply_gates(self, queue):
        # function to apply all the gates
        # queue is the bits for which we know at least one of the inputs
        self.causes = {x: set() for x in self.gates.nodes()}

        for node in queue:
            # find the inputs to the gate that leads to this output
            inputs = list(self.gates.predecessors(node))
            if all([x in self.bits for x in inputs]):
                self.causes[node].update(inputs)
                self.causes[node].update(self.causes[inputs[0]])
                self.causes[node].update(self.causes[inputs[1]])
                
                # if all the inputs for this gate are known, apply the gate
                self.bits[node] = apply_gate[self.gate_types[node]](self.bits[inputs[0]], self.bits[inputs[1]])
                # add the outputs of the gates that have this one as input to the queue
                queue.extend(self.gates.successors(node))

    
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