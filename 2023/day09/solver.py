import sys

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        self.history = []
        for line in self.lines:
            self.history.append(list(map(int, line.strip().split(' '))))

    def find_next_value(self, history, position = -1):
        sequences = [history]

        # calculate the new sequence at each step
        while not all(map(lambda x: x == 0, sequences[-1])):
            sequences.append([])
            i = 0

            # calculate the differences at this step
            while i < (len(sequences[-2]) - 1):
                sequences[-1].append(sequences[-2][i + 1] - sequences[-2][i])
                i += 1

        i = len(sequences) - 1
        # add both the first and last new values to the sequence iteratively
        while i > 0:
            # last value
            sequences[i - 1].append(sequences[i - 1][-1] + sequences[i][-1])

            # first value
            sequences[i - 1].insert(0, sequences[i - 1][0] - sequences[i][0])
            i -= 1

        return sequences[0][position]

    def part1(self):
        total = 0
        for sequence in self.history:
            total += self.find_next_value(sequence)

        return total

    def part2(self):
        total = 0
        for sequence in self.history:
            total += self.find_next_value(sequence, 0)

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