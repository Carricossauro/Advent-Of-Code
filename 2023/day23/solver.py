import sys
from collections import deque

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        self.forest = []
        for line in self.lines:
            self.forest.append(line.strip())

        self.X = len(self.forest)
        self.Y = len(self.forest[0])

    # find all valid adjacent positions
    # if slippery, watch out for slopes
    def adjacent(self, position, slippery):
        x, y = position
        adjacent = []

        if slippery:
            # slopes
            if self.forest[x][y] == '>':
                adjacent.append((x, y + 1))
            elif self.forest[x][y] == '<':
                adjacent.append((x, y - 1))
            elif self.forest[x][y] == '^':
                adjacent.append((x - 1, y))
            elif self.forest[x][y] == 'v':
                adjacent.append((x + 1, y))
            else:
                # no slope
                adjacent.append((x, y + 1))
                adjacent.append((x, y - 1))
                adjacent.append((x - 1, y))
                adjacent.append((x + 1, y))
        else:
            adjacent.append((x, y + 1))
            adjacent.append((x, y - 1))
            adjacent.append((x - 1, y))
            adjacent.append((x + 1, y))

        # filter only valid positions (not out of bounds or a tree)
        return list(filter(lambda p: 0 <= p[0] < self.X and 0 <= p[1] < self.Y and self.forest[p[0]][p[1]] != '#', adjacent))

    # find all paths from start to end
    # works for part 2 in theory but is way too slow
    def find_all_hike_paths(self, start=(0, 1), end=None, slippery=True):
        if end == None:
            end = (self.X - 2, self.Y - 2)

        # BFS
        queue = [(start[0], start[1], 0, [])]
        self.hikes = []
        for x, y, distance, visited in queue:
            if (x, y) == end:
                self.hikes.append(distance + 1)
                continue

            new_visited = visited + [(x, y)]
            for px, py in self.adjacent((x, y), slippery):
                if (px, py) not in visited:
                    queue.append((px, py, distance + 1, new_visited))

    def part1(self):
        self.find_all_hike_paths()

        return max(self.hikes)

    # reduce map to a graph of connected intersections
    # an intersection is a point with >= 3 valid adjacent positions
    # use distance between intersections as edge weights
    def find_intersections(self, start=(0, 1), end=None):
        if end == None:
            end = (self.X - 2, self.Y - 2)

        self.intersections = {}

        # find each intersection
        for x in range(self.X):
            for y in range(self.Y):
                if (self.forest[x][y] != '#' and len(self.adjacent((x, y), False)) > 2) or (x, y) == end or (x, y) == start:
                    self.intersections[(x, y)] = {}

        # find the distance from each intersection to the closest other intersection in each direction
        for intersection in self.intersections.keys():
            # BFS
            queue = [(intersection, 0)]
            visited = set([intersection])
            for position, cost in queue:
                for adjacent_position in self.adjacent(position, False):
                    if adjacent_position not in visited and adjacent_position != start:
                        if adjacent_position in self.intersections:
                            # if found an intersection, update the cost and then stop looking in this direction
                            if adjacent_position not in self.intersections[intersection]:
                                self.intersections[intersection][adjacent_position] = cost + 1
                            else:
                                self.intersections[intersection][adjacent_position] = max(self.intersections[intersection][adjacent_position], cost + 1)
                        else:
                            # if not an intersection, keep looking
                            queue.append((adjacent_position, cost + 1))
                            visited.add(adjacent_position)
            
    # find paths between start and end based on the intersections
    # use distance between intersections as edge weights
    def find_paths_between_intersections(self, start=(0, 1), end=None):
        if end == None:
            end = (self.X - 2, self.Y - 2)
            
        # DFS - shorter memory footprint than BFS
        stack = deque([([start], 1)])
        self.costs = set()
        while stack:
            visited, cost = stack.pop()
            current_intersection = visited[-1]

            if current_intersection == end:
                self.costs.add(cost)
                continue

            for next_intersection in self.intersections[current_intersection].keys():
                if next_intersection not in visited:
                    new_visited = visited + [next_intersection]
                    stack.append((new_visited, cost + self.intersections[current_intersection][next_intersection]))

    def part2(self):
        self.find_intersections()

        self.find_paths_between_intersections()

        return max(self.costs)
    
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