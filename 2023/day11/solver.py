import sys

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        # parsing goes here
        self.universe = [list(line.strip()) for line in self.lines]
        self.X = len(self.universe)
        self.Y = len(self.universe[0])

    # expand the universe
    # would work for part 2 but it becomes too slow
    def cosmic_expansion(self, size = 1):
        # expand empty columns
        i = 0
        while i < len(self.universe[0]):
            # check if column is empty
            if all([row[i] == '.' for row in self.universe]):
                for row in self.universe:
                    for _ in range(size):
                        row.insert(i, '.') # insert empty column
                i += size\

            i += 1

        # expand empty rows
        i = 0
        while i < len(self.universe):
            # check if row is empty
            if self.universe[i].count('#') == 0:
                for _ in range(size):
                    self.universe.insert(i, ['.'] * len(self.universe[0]))
                i += size

            i += 1

        self.X = len(self.universe)
        self.Y = len(self.universe[0])

    # find all galaxies' coordinates
    def find_galaxies(self):
        self.galaxies = []
        for i, row in enumerate(self.universe):
            for j, space in enumerate(row):
                if space == '#':
                    self.galaxies.append((i, j))
        
    def part1(self):
        self.cosmic_expansion()
        self.find_galaxies()
        
        # pure manhattan distance
        # divided by 2 because we count each pair twice
        return sum([abs(galaxy1[0] - galaxy2[0]) + abs(galaxy1[1] - galaxy2[1]) for galaxy1 in self.galaxies for galaxy2 in self.galaxies if galaxy1 != galaxy2]) // 2

    # find rows and columns that require expansion
    def find_expansion_points(self):
        self.expansion_points = {"row": [], "col": []}

        # find expansion points for rows
        for i, row in enumerate(self.universe):
            if row.count('#') == 0:
                self.expansion_points["row"].append(i)

        # find expansion points for columns
        for i in range(self.Y):
            if all([row[i] == '.' for row in self.universe]):
                self.expansion_points["col"].append(i)

    def part2(self):
        self.find_expansion_points()
        self.find_galaxies()

        total = 0
        expansion_level = 1000000
        for x_g1, y_g1 in self.galaxies:
            for x_g2, y_g2 in self.galaxies:
                total_pair = 0
                # check if galaxies expand in rows
                for expansion_x in self.expansion_points["row"]:
                    if x_g1 < expansion_x < x_g2 or x_g2 < expansion_x < x_g1:
                        # artificially add expansion to total
                        total_pair += expansion_level - 1

                # check if galaxies expand in columns
                for expansion_y in self.expansion_points["col"]:
                    if y_g1 < expansion_y < y_g2 or y_g2 < expansion_y < y_g1:
                        # artificially add expansion to total
                        total_pair += expansion_level - 1

                total_pair += abs(x_g1 - x_g2) + abs(y_g1 - y_g2)

                total += total_pair

        # manhattan distance with expansions added artificially
        # divided by 2 because we count each pair twice
        return total // 2

    
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