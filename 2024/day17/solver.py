import sys

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        # parsing goes here
        self.registers = {}
        self.instructions = None

        for line in self.lines:
            if line == "\n":
                continue

            line = line.strip().split(":")

            if line[0][0] == 'R':
                register = line[0].split(" ")[1]
                value = int(line[1].strip())

                self.registers[register] = value
            elif line[0][0] == 'P':
                instructions = line[1].strip().split(",")
                self.instructions = list(map(int, instructions))

        self.N = len(self.instructions)

    def part1(self, as_list=False):
        # part 1 was simple, it's just an implementation of the instructions
        # i should've known what was coming...
        output = []

        i = 0
        while i < self.N - 1:
            instruction = self.instructions[i]
            literal_operand = self.instructions[i + 1]
            combo_operand = self.read_operand(literal_operand)

            if instruction == 0:
                # adv operator
                result = self.registers['A'] // (2 ** combo_operand)
                self.registers['A'] = result
            elif instruction == 1:
                # bxl operator
                result = self.registers['B'] ^ literal_operand
                self.registers['B'] = result
            elif instruction == 2:
                # bst operator
                result = combo_operand % 8
                self.registers['B'] = result
            elif instruction == 3:
                # jnz operator
                if self.registers['A'] != 0:
                    i = literal_operand
                    continue
            elif instruction == 4:
                # bxc operator
                result = self.registers['B'] ^ self.registers['C']
                self.registers['B'] = result
            elif instruction == 5:
                # out operator
                result = combo_operand % 8
                output.append(result)
            elif instruction == 6:
                # bdv operator
                result = self.registers['A'] // (2 ** combo_operand)
                self.registers['B'] = result
            elif instruction == 7:
                # cdv operator
                result = self.registers['A'] // (2 ** combo_operand)
                self.registers['C'] = result

            i += 2

        return output if as_list else ",".join(map(str, output))

    def part2(self):
        # this almost broke me
        # this needs some assumptions
        # 1. every 3 bits of A affect one element of the output (first 3 -> last element, second 3 -> second to last element, etc.)
        # 2. the algorithm will sometimes find dead ends, so it needs to backtrack
        # with both these assumptions made, the algorithm is a bit more simple
        # brute force the first 3 bits of A, then try the next 3 bits, and so on
        # if no combination of the 3 bits gets the correct output, backtrack the previous bits
        # i used a DFS to implement the backtracking
        # every time I move to the next set of bits, I store the used A and output length
        # if it backtracks, it will try the next A with the same output length
        registers = self.registers.copy()

        queue = [(0, 1)] # A, output length
        while queue:
            A, output_length = queue.pop()

            self.registers = registers.copy()
            self.registers['A'] = A

            output = self.part1(as_list=True)
            if len(output) == output_length:
                if output == self.instructions[-output_length:]:
                    if output_length == len(self.instructions):
                        return A
                    queue.append((A + 1, output_length))
                    queue.append((A << 3, output_length + 1))
                elif output[1:] == self.instructions[self.N - output_length + 1:]:
                    queue.append((A + 1, output_length))

    def read_operand(self, operand):
        if 0 <= operand <= 3:
            return operand
        
        if operand == 4:
            return self.registers['A']
        
        if operand == 5:
            return self.registers['B']
        
        if operand == 6:
            return self.registers['C']
    
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