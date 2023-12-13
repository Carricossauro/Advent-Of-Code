import sys
from numpy import floor

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        self.valleys = []
        # valley to be appended to self.valleys
        valley = []
        for line in self.lines:
            if line == "\n":
                # Append valley we just parsed
                self.valleys.append((valley))
                valley = [] # reset valley
            else:
                # Add line to current valley
                valley.append(list(line.strip()))

        # Append last valley
        self.valleys.append(valley)

    # calculates the number of differences between the two sides of the split
    # 0 means the split is mirrored
    def differences_in_split(self, valley, before_split, after_split, vertical=True):
        M = len(valley) if vertical else len(valley[0])

        differences = 0
        for i in range(min(before_split, after_split)):
            for j in range(M):
                if vertical:
                    if valley[j][before_split - i - 1] != valley[j][before_split + i]:
                        differences += 1
                else:
                    if valley[before_split - i - 1][j] != valley[before_split + i][j]:
                        differences += 1

        return differences

    # finds the split with the given number of differences
    # 0 for mirrored split
    # 1 for split with one difference (i.e. the smudge from the problem statement)
    def find_split(self, valley, vertical=True, goal=0):
        start = 1.5
        N = len(valley[0]) if vertical else len(valley)

        while start < N:
            # number of rows/columns before split
            before = int(floor(start))
            # number of rows/columns remaining
            after = N - before

            differences = self.differences_in_split(valley, before, after, vertical)

            if differences == goal:
                break

            start += 1.0

        return int(floor(start)) if differences == goal else None

    # finds the reflections of the valley
    def find_reflections(self):
        self.reflections = [None for _ in self.valleys]

        for i_valley, valley in enumerate(self.valleys):
            # find split vertically
            before_split = self.find_split(valley)
            if before_split:
                self.reflections[i_valley] = ('v', before_split)
            else:
                # find split horizontally
                before_split = self.find_split(valley, vertical=False)
                if before_split:
                    self.reflections[i_valley] = ('h', before_split)

    def part1(self):
        self.find_reflections()

        total = 0
        for reflection in self.reflections:
            if reflection[0] == 'v':
                total += reflection[1]
            else:
                total += reflection[1] * 100
        
        return total

    def part2(self):
        total = 0
        for valley in self.valleys:
            # find split vertically
            split = self.find_split(valley, goal=1)

            if split:
                total += split
            else:
                # find split horizontally
                split = self.find_split(valley, vertical=False, goal=1)

                # check if split was found
                if split:
                    total += split * 100

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