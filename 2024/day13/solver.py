import sys

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        # parsing goes here
        self.machines = [{}]

        for line in self.lines:
            if line == '\n':
                self.machines.append({})
                continue
            before, after = line.split(":")

            if before[0] == 'B':
                movements = after.split(",")
                machine = before[-1]
                x = int(movements[0].split("+")[1])
                y = int(movements[1].split("+")[1])
                self.machines[-1][machine] = (x, y)
            else:
                prizes = after.split(",")
                X = int(prizes[0].split("=")[1])
                Y = int(prizes[1].split("=")[1])
                self.machines[-1]['Prize'] = (X, Y)

    def part1(self):
        # this one was relatively simple, it just required simplifying the equations before coding
        # double equation system
        # X = a * xA + b * xB
        # Y = a * yA + b * yB
        total = 0

        for machine in self.machines:
            xA, yA = machine['A']
            xB, yB = machine['B']
            X, Y = machine['Prize']

            # a post hoc analysis showed that the denominator was never 0
            # "post hoc analysis" is a fancy way of saying
            # "I printed a flag inside this condition and it was never printed"
            if xA * yB - xB * yA == 0:
                continue

            b = (xA * Y - X * yA) // (xA * yB - xB * yA)
            a = (X - b * xB) // xA

            if X == a * xA + b * xB and Y == a * yA + b * yB:
                total += a * 3
                total += b

        return total

    def part2(self):
        # since part 1 was already optimized, this was just a matter of adding the extra requirements
        total = 0

        for machine in self.machines:
            xA, yA = machine['A']
            xB, yB = machine['B']
            X, Y = machine['Prize']
            X += 10000000000000
            Y += 10000000000000

            if xA * yB - xB * yA == 0:
                continue

            b = (xA * Y - X * yA) // (xA * yB - xB * yA)
            a = (X - b * xB) // xA

            if X == a * xA + b * xB and Y == a * yA + b * yB:
                total += a * 3
                total += b

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