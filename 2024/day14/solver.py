import sys

from math import prod
from tqdm import tqdm

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        # parsing goes here
        self.robots = []
        if file_path == "test.txt":
            self.X = 11
            self.Y = 7
        else:
            self.X = 101
            self.Y = 103

        for line in self.lines:
            position, velocity = line.strip().split(" ")
            [x, y] = position[2:].split(',')
            [vx, vy] = velocity[2:].split(',')

            self.robots.append({
                'x': int(x),
                'y': int(y),
                'vx': int(vx),
                'vy': int(vy)
            })

        self.N = len(self.robots)

    def part1(self):
        # this part was easy, just uso modulo to calculate the final positions
        # and then check each quadrant
        # there might have been an easier way to check the quadrants
        seconds = 100

        final_positions = {}
        for robot in self.robots:
            x, y = robot['x'], robot['y']
            vx, vy = robot['vx'], robot['vy']

            position = ((x + vx * seconds) % self.X, (y + vy * seconds) % self.Y)

            if position not in final_positions:
                final_positions[position] = 0
            final_positions[position] += 1


        quadrants = [0, 0, 0, 0]
        quadrant_limits = [((0, self.X // 2),(0, self.Y // 2)),
                           ((0, self.X // 2),(self.Y // 2 + 1, self.Y)),
                           ((self.X // 2 + 1, self.X),(0, self.Y // 2)),
                           ((self.X // 2 + 1, self.X),(self.Y // 2 + 1, self.Y))]

        for i, quadrant_limit in enumerate(quadrant_limits):
            x1, x2 = quadrant_limit[0]
            y1, y2 = quadrant_limit[1]

            for x in range(x1, x2):
                for y in range(y1, y2):
                    if (x, y) in final_positions:
                        quadrants[i] += final_positions[(x, y)]

        return prod(quadrants)
    
    def part2(self):
        # i didn't like this part, this just requires actually looking at it manually
        # it CAN be done programmatically, but it's clearly not made for that
        # and it would be too much unnecessary work
        with open("out.txt", "w") as file:
            for second in tqdm(range(self.X * self.Y)):
                positions = {}
                for i, robot in enumerate(self.robots):
                    x, y = robot['x'], robot['y']
                    vx, vy = robot['vx'], robot['vy']

                    position = ((x + vx) % self.X, (y + vy) % self.Y)
                    self.robots[i] = {
                        'x': position[0],
                        'y': position[1],
                        'vx': vx,
                        'vy': vy
                    }

                    if position not in positions:
                        positions[position] = 0
                    positions[position] += 1
                    
                file.write("-------------------------------------------\n")
                file.write(f"Second {second + 1}\n")
                file.write("-------------------------------------------\n")
                for y in range(self.Y):
                    for x in range(self.X):
                        if (x, y) in positions:
                            file.write('#')
                        else:
                            file.write('.')
                    file.write("\n")

        return "Check out.txt"
    
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