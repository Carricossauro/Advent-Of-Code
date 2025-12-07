import sys

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        # parsing goes here
        self.rows = len(self.lines)
        self.cols = len(self.lines[0].strip())
        self.grid = []
        self.start = None
        for r, line in enumerate(self.lines):
            self.grid.append(line.strip())

            for c, char in enumerate(line.strip()):
                if char == 'S':
                    self.start = (r, c)

    def part1(self):
        beams = set([self.start])
        splits = 0
        visited = set([self.start])

        while beams:
            new_beams = set()
            for r, c in beams:
                # process each beam
                nr = r + 1
                if 0 <= nr < self.rows:
                    if self.grid[nr][c] == "^":
                        splits += 1
                        lc = c - 1
                        rc = c + 1
                        if 0 <= lc < self.cols and (r, lc) not in visited:
                            new_beams.add((r, lc))  # split left
                            visited.add((r, lc))
                        if 0 <= rc < self.cols and (r, rc) not in visited:
                            new_beams.add((r, rc))  # split right
                            visited.add((r, rc))
                    elif (nr, c) not in visited:
                        new_beams.add((nr, c))  # continue down
                        visited.add((nr, c))

            beams = new_beams
        return splits

    def part2(self):
        # instead of counting beam individualy, count the timelines for each position
        beams = {self.start: 1}
        timelines = 1

        while beams:
            new_beams = {} # this will replace the beams dict
            for r, c in beams:
                # process each beam
                b = self.move_beam(r, c)
                if len(b) > 1:
                    # if the beams split, we double the timelines in this position
                    timelines += beams[(r, c)]
                for nr, nc in b:
                    # add the correct number of beams to the new position
                    if (nr, nc) not in new_beams:
                        new_beams[(nr, nc)] = 0
                    new_beams[(nr, nc)] += beams[(r, c)]
            beams = new_beams

        return timelines
    
    def move_beam(self, r, c):
        # initialy tried to use lru_cache, but it was still too slow
        beams = []

        nr = r + 1
        if 0 <= nr < self.rows:
            if self.grid[nr][c] == "^":
                lc = c - 1
                rc = c + 1
                if 0 <= lc < self.cols:
                    beams.append((r, lc))  # split left
                if 0 <= rc < self.cols:
                    beams.append((r, rc))  # split right
            else:
                beams.append((nr, c))  # continue down

        return beams
    
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