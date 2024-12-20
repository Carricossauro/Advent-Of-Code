import sys

from collections import Counter

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        # parsing goes here
        self.map = []
        self.start = None
        self.end = None

        for i, line in enumerate(self.lines):
            self.map.append([])
            for j, cell in enumerate(line.strip()):
                if cell == 'S':
                    self.start = (i, j)
                    self.map[i].append('.')
                elif cell == 'E':
                    self.end = (i, j)
                    self.map[i].append('.')
                else:
                    self.map[i].append(cell)

        self.N = len(self.map)
        self.M = len(self.map[0])

        self.is_testing = file_path.startswith("test")

    def part1(self):
        # since the cheats are only length 2 (cross only one wall), we can just hard code the checking of cheats
        # start by calculating the race path and the distance to every cell in that path
        # then iterate through the path and check for possible cheats
        distances = {}
        distances[self.start] = 0

        # find the best path and the distance to every cell
        # this isn't really a map seach since there is only one path
        # it just follows the path and records the distance from the start to each cell
        position = self.start
        distance = 0
        original_path = set([self.start])
        while position != self.end:
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_x, new_y = position[0] + dx, position[1] + dy
                new_position = (new_x, new_y)

                if 0 <= new_x < self.N and 0 <= new_y < self.M and self.map[new_x][new_y] == '.' and new_position not in original_path:
                    distance += 1
                    distances[new_position] = distance
                    
                    original_path.add(new_position)
                    position = new_position

        # iterate through the best path, find where there could be cheats
        cheats = {}
        for position in original_path:
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                cheat_start = position[0] + dx, position[1] + dy

                # check if the cheat start position is within the map and not in the original path
                if cheat_start not in original_path and 0 <= cheat_start[0] < self.N and 0 <= cheat_start[1] < self.M:
                    cheat_end = cheat_start[0] + dx, cheat_start[1] + dy

                    # check if the cheat end position is in the original path
                    if cheat_end in original_path:
                        cheat_end_distance = distances[position] + 2
                        new_distance = distances[self.end] - distances[cheat_end] + cheat_end_distance
                        
                        # check if the new distance is less than the original distance to the end position
                        if new_distance < distances[self.end]:
                            cheats[(cheat_start, cheat_end)] = new_distance

        if self.is_testing:
            return Counter(map(lambda x: distances[self.end] - x, cheats.values()))

        return sum(Counter(filter(lambda x: x >= 100, map(lambda x: distances[self.end] - x, cheats.values()))).values())

    def part2(self):
        # this part ended up being so much easier than what I made it out to be
        # wasted so much time trying map search algorithms
        # the solution is to just brute force all the possible cheat starting positions and distances to end positions
        cheat_limit = 20
        time_to_save = 50 if self.is_testing else 100 

        distances = {}
        distances[self.start] = 0

        # find the best path and the distance to every cell
        # this isn't really a map seach since there is only one path
        # it just follows the path and records the distance from the start to each cell
        position = self.start
        distance = 0
        original_path = set([self.start])
        while position != self.end:
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_x, new_y = position[0] + dx, position[1] + dy
                new_position = (new_x, new_y)

                if 0 <= new_x < self.N and 0 <= new_y < self.M and self.map[new_x][new_y] == '.' and new_position not in original_path:
                    distance += 1
                    distances[new_position] = distance
                    
                    original_path.add(new_position)
                    position = new_position
        
        total = 0
        # find all possible end cheat positions for each start position
        # literally just brute force all the end positions with manhattan distance <= cheat_limit (20)
        for cheat_start in original_path:
            for dx in range(-cheat_limit, cheat_limit + 1):
                for dy in range(-cheat_limit, cheat_limit + 1):
                    x, y = cheat_start[0] + dx, cheat_start[1] + dy
                    cheat_end = (x, y)

                    # check if the end position is in the path
                    # only situation where the end position for a cheat is valid
                    if cheat_end in original_path:
                        cheat_distance = abs(x - cheat_start[0]) + abs(y - cheat_start[1])
                        distance_to_cheat_end = distances[cheat_start] + cheat_distance

                        # check if new calculated distance (with the cheat) is within the limit and less than the original distance to that position
                        # basically check if the cheat actually saves time
                        if cheat_distance <= cheat_limit and distance_to_cheat_end < distances[cheat_end]:
                            distance_to_end = distances[self.end] - distances[cheat_end] + distance_to_cheat_end

                            # only count if the cheat actually saves the time we want to count
                            if distance_to_end <= distances[self.end] - time_to_save:
                                total += 1

        return total
    
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