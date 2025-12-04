import sys

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        # parsing goes here
        self.grid = []
        for line in self.lines:
            self.grid.append([x for x in line.strip()])

        self.Y = len(self.grid)
        self.X = len(self.grid[0])

    def can_be_accessed(self, x, y):
        # function that checks the adjacent cells and counts the rolls
        ds = [-1, 0, 1]

        rolls = 0
        for dx in ds:
            for dy in ds:
                if dx == 0 and dy == 0:
                    continue

                if 0 <= x + dx < self.X and 0 <= y + dy < self.Y:
                    if self.grid[y + dy][x + dx] == '@':
                        rolls += 1
                
        return rolls < 4

    def part1(self):
        # go through each position and see if it can be accessed
        accessible_count = 0
        for x in range(self.X):
            for y in range(self.Y):
                if self.grid[y][x] == '@':
                    if self.can_be_accessed(x, y):
                        accessible_count += 1

        return accessible_count

    def part2(self):
        # go through each position and see if it can be accessed
        # repeat until a whole pass is made with no changes
        accessible_count = 0
        changing = True
        while changing:
            changing = False
            for x in range(self.X):
                for y in range(self.Y):
                    if self.grid[y][x] == '@':
                        if self.can_be_accessed(x, y):
                            self.grid[y][x] = 'x'
                            accessible_count += 1
                            changing = True
        return accessible_count
    
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