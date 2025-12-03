import sys

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        # parsing goes here
        self.ranges = []
        line = self.lines[0].strip().split(",")
        for r in line:
            a, b = r.split("-")
            self.ranges.append((int(a), int(b)))

    def part1(self):
        invalids = 0
        for id_range in self.ranges:
            for id in range(id_range[0], id_range[1] + 1):
                string_id = str(id)
                half = len(string_id) // 2
                first_half = string_id[:half]
                second_half = string_id[half:]
                if first_half == second_half:
                    invalids += id

        return invalids

    def part2(self):
        invalids = 0
        for id_range in self.ranges:
            for id in range(id_range[0], id_range[1] + 1):
                string_id = str(id)
                for length in range(1, len(string_id) // 2 + 1):
                    parts = [string_id[i:i+length] for i in range(0, len(string_id), length)]
                    if all(part == parts[0] for part in parts):
                        invalids += id
                        break

        return invalids
    
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