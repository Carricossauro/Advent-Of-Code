import sys
import networkx

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        self.wires = {}
        for line in self.lines:
            [wire, connections] = line.strip().split(":")
            if wire not in self.wires:
                self.wires[wire] = []

            # connect all wires bidirectionally
            for connection in connections.strip().split():
                self.wires[wire].append(connection.strip())
                if connection not in self.wires:
                    self.wires[connection] = []
                self.wires[connection].append(wire)

    # nothing to say here, the code is simple enough
    def part1(self):
        G = networkx.Graph()

        for wire in self.wires:
            for connection in self.wires[wire]:
                G.add_edge(wire, connection)

        cc = networkx.spectral_bisection(G)
        return len(cc[0]) * len(cc[1])

    def part2(self):
        return None
    
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