import sys

# direction vectors to simplify adjacent cell calculation
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        # parsing goes here
        self.map = []
        self.trailheads = []
        self.N = len(self.lines)
        self.M = len(self.lines[0].strip())

        for i, line in enumerate(self.lines):
            self.map.append([])
            for j, char in enumerate(line.strip()):
                self.map[-1].append(int(char))
                if char == '0':
                    self.trailheads.append((i, j))

    def part1(self):
        # DFS solution
        # used DFS since we have to check everything anyway
        # i usually like BFS for map problems but it would have been unnecessary
        scores = {x:0 for x in self.trailheads}
        visited = {x:set() for x in self.trailheads}

        # queue starts at all trailheads
        queue = [(x, x) for x in self.trailheads] # (start, current)
        while queue:
            start, current = queue.pop()
            if current not in visited[start]:
                visited[start].add(current)

                if self.map[current[0]][current[1]] == 9:
                    # if reached the end of the trail, increment score
                    # only does it once per trailhead/end combination because of visited set
                    scores[start] += 1
                else:
                    # check all 4 adjacent cells
                    for direction in DIRECTIONS:
                        next = (current[0] + direction[0], current[1] + direction[1])
                        if 0 <= next[0] < self.N and 0 <= next[1] < self.M and next not in visited[start] and self.map[next[0]][next[1]] == self.map[current[0]][current[1]] + 1:
                            queue.append((start, next))
                        
        return sum(scores.values())

    def part2(self):
        # same DFS solution
        scores = {x:0 for x in self.trailheads}

        # queue starts at all trailheads
        queue = [(x, x, set()) for x in self.trailheads] # (start, current, visited)
        while queue:
            start, current, visited = queue.pop()
            if current not in visited:
                new_visited = visited.copy()
                new_visited.add(current)

                if self.map[current[0]][current[1]] == 9:
                    # if reached the end of the trail, increment score
                    # checks each end of trail (possibly) more than once
                    # once for each path from a trailhead to the end
                    # because visited set is now per path
                    scores[start] += 1
                else:
                    # check all 4 adjacent cells
                    for direction in DIRECTIONS:
                        next = (current[0] + direction[0], current[1] + direction[1])
                        if 0 <= next[0] < self.N and 0 <= next[1] < self.M and next not in visited and self.map[next[0]][next[1]] == self.map[current[0]][current[1]] + 1:
                            queue.append((start, next, new_visited))
                        
        return sum(scores.values())
    
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