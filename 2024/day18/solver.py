import sys

FREE = 0
OBSTACLE = 1

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        # parsing goes here
        self.testing = file_path == "test.txt"

        # 0 to 6 and 0 to 70 was tricky wording, good thing I caught it early
        self.N = 7 if self.testing else 71

        self.bytes = []
        for line in self.lines:
            x, y = line.strip().split(',')
            # i switched x and y here because I'm more used to (x, y) coordinates
            # this was just to avoid stupid mistakes on my part
            self.bytes.append((int(y), int(x)))

        self.grid = [[FREE] * self.N for _ in range(self.N)]

    def part1(self):
        # simple part 1
        # just a map search with the the simulation of the first bytes beforehand
        fallen_bytes = 12 if self.testing else 1024
        
        # simulate the falling of the first bytes
        self.simulate_fallen_bytes(0, fallen_bytes)

        # find the shortest path and return the distance
        return self.find_new_path()[0]

    def part2(self):
        # a bit more complicated, but still not that hard
        # find the path, iterate through the falling bytes until one of them is in the path
        # then simulate the falling of all the bytes up to that point
        # when the path is empty, we have found the first byte that actually blocks the exit
        fallen_bytes = 0
        
        path = self.find_new_path()[1]
        for i, (x, y) in enumerate(self.bytes):
            if (x, y) in path:
                # if the byte is in the path, simulate the falling of all the bytes up to that point
                fallen_bytes = self.simulate_fallen_bytes(fallen_bytes, i - fallen_bytes + 1)

                # find the new path
                path = self.find_new_path()[1]
                if path == set():
                    # if the path is empty, we have found the first byte that actually blocks the exit
                    return ",".join(map(str, [y, x]))

        return None
    
    def find_new_path(self):
        # basically a BFS with a DP table for shortest distance found
        # updates queue for every new cell with a new lowest distance
        # visited to keep path for part 2
        distances = {(x, y) : (float("inf"), set()) for x in range(self.N) for y in range(self.N)}
        distances[(0, 0)] = (0, set())

        queue = [(0, 0, 0, set())] # x, y, distance, visited
        for x, y, distance, visited in queue:
            new_distance = distance + 1
            new_visited = visited.copy()
            new_visited.add((x, y))

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < self.N and 0 <= new_y < self.N and self.grid[new_x][new_y] == FREE and (new_x, new_y) not in visited:
                    if distances[(new_x, new_y)][0] > new_distance:
                        distances[(new_x, new_y)] = (new_distance, new_visited)
                        if (new_x, new_y) != (self.N - 1, self.N - 1):
                            queue.append((new_x, new_y, new_distance, new_visited))

        return distances[(self.N - 1, self.N - 1)]
    
    def simulate_fallen_bytes(self, fallen_bytes_start, fallen_bytes_length):
        # simple simulation of the falling bytes
        # iterate throught the ones we want and place them on the grid
        for i in range(fallen_bytes_start, fallen_bytes_start + fallen_bytes_length):
            x, y = self.bytes[i]
            self.grid[x][y] = OBSTACLE

        return fallen_bytes_start + fallen_bytes_length
    
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