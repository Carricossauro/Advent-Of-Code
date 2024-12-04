import sys

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        # parsing goes here
        self.word_search = []
        for line in self.lines:
            self.word_search.append(list(line.strip()))

        self.N = len(self.word_search)
        self.M = len(self.word_search[0])

        self.next_step = {'X': 'M', 'M': 'A', 'A': 'S', 'S': 'X'}

    def part1(self):
        found_occurrences = 0

        # horizontal
        for i in range(self.N):
            step = 'X'
            for j in range(self.M):
                if self.word_search[i][j] == 'X':
                    step = 'M'
                elif self.word_search[i][j] == step:
                    if step == 'S':
                        found_occurrences += 1
                    step = self.next_step[step]
                else:
                    step = 'X'

        # horizontal reversed
        for i in range(self.N - 1, -1, -1):
            step = 'X'
            for j in range(self.M - 1, -1, -1):
                if self.word_search[i][j] == 'X':
                    step = 'M'
                elif self.word_search[i][j] == step:
                    if step == 'S':
                        found_occurrences += 1
                    step = self.next_step[step]
                else:
                    step = 'X'

        # vertical
        for j in range(self.M):
            step = 'X'
            for i in range(self.N):
                if self.word_search[i][j] == 'X':
                    step = 'M'
                elif self.word_search[i][j] == step:
                    if step == 'S':
                        found_occurrences += 1
                    step = self.next_step[step]
                else:
                    step = 'X'

        # vertical reversed
        for j in range(self.M - 1, -1, -1):
            step = 'X'
            for i in range(self.N - 1, -1, -1):
                if self.word_search[i][j] == 'X':
                    step = 'M'
                elif self.word_search[i][j] == step:
                    if step == 'S':
                        found_occurrences += 1
                    step = self.next_step[step]
                else:
                    step = 'X'

        # diagonal left to right
        start_points = [(0, j) for j in range(self.M)] + [(i, 0) for i in range(1, self.N)]
        for start in start_points:
            step = 'X'
            i, j = start
            while i < self.N and j < self.M:
                if self.word_search[i][j] == 'X':
                    step = 'M'
                elif self.word_search[i][j] == step:
                    if step == 'S':
                        found_occurrences += 1
                    step = self.next_step[step]
                else:
                    step = 'X'
                i += 1
                j += 1

        # diagonal left to right reversed
        start_points = [(self.N - 1, j) for j in range(self.M)] + [(i, self.M - 1) for i in range(self.N - 1)]
        for start in start_points:
            step = 'X'
            i, j = start
            while i >= 0 and j >= 0:
                if self.word_search[i][j] == 'X':
                    step = 'M'
                elif self.word_search[i][j] == step:
                    if step == 'S':
                        found_occurrences += 1
                    step = self.next_step[step]
                else:
                    step = 'X'
                i -= 1
                j -= 1

        # diagonal right to left
        start_points = [(0, j) for j in range(self.M)] + [(i, self.M - 1) for i in range(1, self.N)]
        for start in start_points:
            step = 'X'
            i, j = start
            while i < self.N and j >= 0:
                if self.word_search[i][j] == 'X':
                    step = 'M'
                elif self.word_search[i][j] == step:
                    if step == 'S':
                        found_occurrences += 1
                    step = self.next_step[step]
                else:
                    step = 'X'
                i += 1
                j -= 1

        # diagonal right to left reversed
        start_points = [(self.N - 1, j) for j in range(self.M)] + [(i, 0) for i in range(self.N - 1)]
        for start in start_points:
            step = 'X'
            i, j = start
            while i >= 0 and j < self.M:
                if self.word_search[i][j] == 'X':
                    step = 'M'
                elif self.word_search[i][j] == step:
                    if step == 'S':
                        found_occurrences += 1
                    step = self.next_step[step]
                else:
                    step = 'X'
                i -= 1
                j += 1

        return found_occurrences
    
    def part2(self):
        # loop through the centers of the X-MAS and then check if the diagonals are correct
        x_center = [(i, j) for i in range(1, self.N - 1) for j in range(1, self.M - 1) if self.word_search[i][j] == 'A']
        found_occurrences = 0

        for i, j in x_center:
            mas = 0
            if self.word_search[i - 1][j - 1] == 'M' and self.word_search[i + 1][j + 1] == 'S':
                mas += 1
            elif self.word_search[i - 1][j - 1] == 'S' and self.word_search[i + 1][j + 1] == 'M':
                mas += 1

            if self.word_search[i - 1][j + 1] == 'M' and self.word_search[i + 1][j - 1] == 'S':
                mas += 1
            if self.word_search[i - 1][j + 1] == 'S' and self.word_search[i + 1][j - 1] == 'M':
                mas += 1

            if mas == 2:
                found_occurrences += 1

        return found_occurrences
    
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