import sys

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        # parsing goes here
        self.ranges = []
        self.ingredients = []
        ingredients = False
        for line in self.lines:
            line = line.strip()
            if line == "":
                ingredients = True
                continue
            if not ingredients:
                self.ranges.append(list(map(int, line.split("-"))))
            else:
                self.ingredients.append(int(line))

    def part1(self):
        total = 0

        for ingredient in self.ingredients:
            valid = False
            for r in self.ranges:
                if r[0] <= ingredient <= r[1]:
                    valid = True
                    break
            if valid:
                total += 1

        return total

    def part2(self):
        # sort ranges
        self.ranges.sort()

        # merge overlapping ranges
        merged_ranges = [self.ranges[0]]
        i = 1
        while i < len(self.ranges):
            current_range = self.ranges[i]
            last_merged_range = merged_ranges[-1]

            if current_range[0] <= last_merged_range[1]:
                last_merged_range[1] = max(last_merged_range[1], current_range[1])
            else:
                merged_ranges.append(current_range)

            i += 1
            
        # count possible fresh ingredients within merged ranges
        total = 0
        for range in merged_ranges:
            total += range[1] - range[0] + 1

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
            print("\nPart 1:", solver.part1())
        else:
            print("\nPart 2:", solver.part2())
    else:
        print("Usage: python3 solver.py [1 / 2] [test / test2 / 1 / 2]")
        print("Filenames: test.txt\n\t   test2.txt\n\t   input1.txt\n\t   input2.txt")