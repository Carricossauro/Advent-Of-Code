import sys

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        # parsing goes here
        self.memory = []
        for line in self.lines:
            self.memory.append(line.strip())

    def part1(self):
        total = 0
        for instructions in self.memory:
            step = 'm' # can be 'm', 'u', 'l', '(', '1', '2'
            n1 = ""
            n2 = ""

            i = 0
            N = len(instructions)
            while i < N:
                if step == 'm' and instructions[i] == 'm':
                    step = 'u'
                elif step == 'u' and instructions[i] == 'u':
                    step = 'l'
                elif step == 'l' and instructions[i] == 'l':
                    step = '('
                elif step == '(' and instructions[i] == '(':
                    step = '1'
                elif step == '1' and instructions[i].isdigit() and len(n1) < 3:
                    n1 += instructions[i]
                elif step == '1' and instructions[i] == ',' and len(n1) > 0:
                    step = '2'
                elif step == '2' and instructions[i].isdigit() and len(n2) < 3:
                    n2 += instructions[i]
                elif step == '2' and instructions[i] == ')' and len(n2) > 0:
                    total += int(n1) * int(n2)
                    n1 = ""
                    n2 = ""
                    step = 'm'
                else:
                    step = 'm'
                    n1 = ""
                    n2 = ""

                i += 1

        return total

    def part2(self):
        total = 0
        enabled = True
        for instructions in self.memory:
            # step will move accoding to the instruction if it finds the correct characters
            # 'd' -> 'o' -> '(' -> done
            # 'd' -> 'n' -> "'" -> 't' -> '(' -> done
            # 'm' -> 'u' -> 'l' -> '(' -> '1' -> ',' -> '2' -> done
            step = ''
            n1 = ""
            n2 = ""
            do = False
            dont = False
            mul = False

            i = 0
            N = len(instructions)
            while i < N:
                if instructions[i] in ['d', 'm']: # if found first letter of instruction, reset search
                    step = instructions[i]
                    do = False
                    dont = False
                    mul = False
                elif instructions[i] == 'o' and step == 'd':
                    step = 'o'
                    do = True
                elif instructions[i] == 'n' and step == 'o':
                    step = 'n'
                    do = False
                elif instructions[i] == "'" and step == 'n':
                    step = "'"
                elif instructions[i] == 't' and step == "'":
                    step = 't'
                    dont = True
                elif instructions[i] == 'u' and step == 'm':
                    step = 'u'
                elif instructions[i] == 'l' and step == 'u':
                    step = 'l'
                    mul = True
                elif instructions[i] == '(' and any([do, dont, mul]):
                    step = '('
                elif instructions[i].isdigit() and mul and step == '(' and len(n1) < 3:
                    n1 += instructions[i]
                elif instructions[i] == ',' and mul and step == '(' and len(n1) > 0:
                    step = ','
                elif instructions[i].isdigit() and mul and step == ',' and len(n2) < 3:
                    n2 += instructions[i]
                elif instructions[i] == ')' and mul and step == ',' and len(n2) > 0 and enabled:
                    total += int(n1) * int(n2)
                    n1 = ""
                    n2 = ""
                    step = ''
                    mul = False
                elif instructions[i] == ')' and do:
                    enabled = True
                    step = ''
                elif instructions[i] == ')' and dont:
                    enabled = False
                    step = ''
                else:
                    step = ''
                    n1 = ""
                    n2 = ""
                    do = False
                    dont = False
                    mul = False

                i += 1

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