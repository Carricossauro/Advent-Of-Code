import sys

import networkx as nx

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        # parsing goes here
        self.graph = nx.Graph()

        for line in self.lines:
            nodes = line.strip().split("-")

            self.graph.add_edge(nodes[0], nodes[1])

    def part1(self):
        # did this manually becasue it's more interesting
        # basically a BFS search with a distance limit
        # finds all loops of length 3 (where the 4th element is the same as the 1st)
        # only starts in nodes starting with 't' to preemtively reduce the search space to possible results
        # too slow for part 2
        groups = set()

        queue = [(x, x, 1, set()) for x in self.graph.nodes() if x.startswith('t')]
        for start, node, distance, visited in queue:
            if distance == 4:
                # stop if we reached the 4th node
                if node == start:
                    # add the group to the set if it reached the start again
                    groups.add(tuple(sorted(list(visited))))
                continue

            for neighbor in self.graph.neighbors(node):
                if neighbor not in visited:
                    queue.append((start, neighbor, distance + 1, visited | {neighbor}))

        return len(groups)
    
    def part2(self):
        # felt lazy
        # nx.find_cliques finds all complete subgraphs of the graph
        # then just return the largest one
        cliques = list(nx.find_cliques(self.graph))

        return ",".join(sorted(max(cliques, key=len)))
    
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