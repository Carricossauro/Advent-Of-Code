import sys

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        # parsing goes here
        self.joltages = [list(map(int, list(line.strip( )))) for line in self.lines]

    def part1(self):
        # simple solution
        # just find the two largest numbers that are in increasing order
        output_joltage = 0

        for joltage in self.joltages:
            n1 = joltage[0]
            n2 = joltage[1]

            for i, jolt in enumerate(joltage[1:]):
                # i + 2 is used here since the "enumerate" starts from the second element (usually would be i + 1)
                if jolt > n1 and i + 2 < len(joltage):
                    # found a new overall largest, change n1 and set n2 to the next number
                    # only applicable if there is a next number left
                    n1 = jolt
                    n2 = joltage[i + 2]
                elif jolt > n2:
                    # found a new second largest that is still smaller than the current n1
                    n2 = jolt
            
            output_joltage += n1 * 10 + n2

        return output_joltage

    def part2(self):
        # this needs a greedy approach since the larger digits are more important
        # greedy approach takes the largest digit possible for each position
        # then starts searching again from the next position
        output_joltage = 0

        for joltage in self.joltages:
            digits = []

            max_digit = -1
            max_position = -1
            for position in range(12):
                # about [:len(joltage) - 12 + 1 + position]
                # "position" digits are filled, we are filling the next one
                # so we need to leave enough digits for the remaining positions
                for j, jolt in enumerate(joltage[:len(joltage) - 12 + 1 + position]):
                    # next digit needs to come after the last used digit
                    if j > max_position and jolt > max_digit:
                        # if it is a valid position and larger than current max, update
                        max_digit = jolt
                        max_position = j

                digits.append(max_digit)
                max_digit = -1 # reset since the comparisons are unique per position
            
            output_joltage += int(''.join(map(str, digits)))

        return output_joltage
    
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