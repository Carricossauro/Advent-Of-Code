import sys

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        # parsing goes here
        self.movements = []
        for line in self.lines:
            direction = line[0]
            number = int(line[1:])
            self.movements.append((direction, number))

    def part1(self):
        dial = 50
        count = 0
        for direction, number in self.movements:
            if direction == 'L':
                dial -= number
            else:
                dial += number

            dial %= 100
            if dial == 0:
                count += 1

        return count

    def part2(self):
        dial = 50
        count = 0
        for direction, number in self.movements:
            
            count += abs(number // 100) # count full rotations
            remove = -1 if dial == 0 else 0 # adjust for starting the round at 0 to avoid double counting

            if direction == 'L':
                dial -= number % 100
            else:
                dial += number % 100

            if dial <= 0 or dial >= 100:
                count += 1 + remove # count final crossing if applicable and remove adjustment
            dial %= 100

        return count
    
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