import sys

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        # parsing goes here
        self.operations = {}
        for line in self.lines[:-1]:
            line = line.strip()
            
            for i, number in enumerate(line.split()):
                if i not in self.operations:
                    self.operations[i] = []
                self.operations[i].append(int(number))

        for i, operation in enumerate(self.lines[-1].split()):
            if i not in self.operations:
                self.operations[i] = []
            self.operations[i].append(operation)     

    def part1(self):
        total = 0
        
        for i, operation in self.operations.items():
            if operation[-1] == '*':
                result = 1
                for number in operation[:-1]:
                    result *= number
                total += result
            elif operation[-1] == '+':
                result = 0
                for number in operation[:-1]:
                    result += number
                total += result

        return total

    def part2(self):
        # treated the full raw input as a matrix to simplify the logic
        # reparsed the input by columns
        # fix the column, move down the rows to get numbers
        # only store a number when you hit the final row and change the operation when necessary
        COLUMNS = max(map(len, self.lines))
        ROWS = len(self.lines)
        operations = {}
        current_op = -1
        operation = None
        for column in range(COLUMNS):
            number = ""
            for row in range(ROWS):
                if column >= len(self.lines[row]): # control for uneven row lengths
                    continue

                char = self.lines[row][column]
                if row == ROWS - 1:
                    if char in ['*', '+']:
                        if current_op >= 0: # control for initial definition of the variable
                            operations[current_op].append(operation)
                        operation = char
                        current_op += 1
                        operations[current_op] = []
                    if number: # control for the blank columns
                        operations[current_op].append(int(number))
                else:
                    if char != ' ': # control for extra spaces after/before numbers
                        number += char
        operations[current_op].append(operation) # this is a bit of a hacky fix but it works for the input

        # then just reuse part1 logic with the new operations
        self.operations = operations
        return self.part1()
    
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