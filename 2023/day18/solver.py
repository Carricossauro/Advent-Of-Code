import sys

RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3
directions = {"U": UP, "R": RIGHT, "D": DOWN, "L": LEFT}

VERTICAL = 4
HORIZONTAL = 5
CORNER = 6

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        self.dig_plan = []
        self.altered_dig_plan = []
        for line in self.lines:
            direction, length, color = line.strip().split()
            self.dig_plan.append((directions[direction], int(length)))

            altered_direction = int(color[-2])
            altered_length = int(color[2:-2], 16)
            self.altered_dig_plan.append((altered_direction, altered_length))

    # simple enough
    # move across the dig plan and record vertices
    def find_vertices(self):
        self.vertices = [(0,0)]
        x, y = 0, 0
        smallest_x, smallest_y = float("inf"), float("inf")

        for direction, length in self.dig_plan:
            if direction == RIGHT:
                y += length
            elif direction == LEFT:
                y -= length
            elif direction == UP:
                x -= length
            elif direction == DOWN:
                x += length

            self.vertices.append((x, y))

            smallest_x = min(smallest_x, x)
            smallest_y = min(smallest_y, y)
    
    # shoelace formula
    def calculate_area(self):
        xs = [x for x, _ in self.vertices]
        ys = [y for _, y in self.vertices]

        area = 0
        for i in range(len(self.vertices) - 1):
            area += xs[i] * ys[i + 1] - xs[i + 1] * ys[i]

        return abs(area // 2)
    
    # pick's theorem
    def calculate_inner_points(self):
        self.A = self.calculate_area()
        self.b = sum(x[1] for x in self.dig_plan)

        return self.A - (self.b // 2) + 1
    
    # i + b from pick's theorem
    # inner points + boundary points
    def calculate_total_points(self):
        return self.calculate_inner_points() + self.b

    def part1(self):
        self.find_vertices()

        return self.calculate_total_points()

    def part2(self):
        self.dig_plan = self.altered_dig_plan

        return self.part1()
    
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