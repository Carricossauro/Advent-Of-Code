import sys
from math import floor, log10

operations = [
    lambda x, y: x + y,                                 # add
    lambda x, y: x * y,                                 # multiply
    lambda x, y: x * ( 10**( floor(log10(y)) + 1) ) + y # concatenate
]

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        # parsing goes here
        self.equations = []
        for line in self.lines:
            result, numbers = line.strip().split(":")
            numbers = list(map(int, numbers.strip().split(" ")))
            self.equations.append((int(result), numbers))

    def part1(self):
        res = 0

        for result, numbers in self.equations:
            queue = [(1, numbers[0])] # (index, result)
            found = False

            for i, total in queue:
                if found:
                    break
                else:
                    for op in operations[:2]:
                        new_total = op(total, numbers[i])
                        if i == len(numbers) - 1:
                            if new_total == result:
                                res += new_total
                                found = True
                                break
                        elif new_total <= result:
                            queue.append((i + 1, new_total))

        return res

    def part2(self):
        res = 0

        for result, numbers in self.equations:
            queue = [(1, numbers[0])] # (index, result)
            found = False

            for i, total in queue:
                if found:
                    break
                else:
                    for op in operations:
                        new_total = op(total, numbers[i])
                        if i == len(numbers) - 1:
                            if new_total == result:
                                res += new_total
                                found = True
                                break
                        elif new_total <= result:
                            queue.append((i + 1, new_total))

        return res
    
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