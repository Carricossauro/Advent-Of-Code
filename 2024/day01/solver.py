import sys

class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        # parsing goes here
        self.list_1 = []
        self.list_2 = []
        
        for line in self.lines:
            numbers = line.split()
            self.list_1.append(int(numbers[0]))
            self.list_2.append(int(numbers[1]))

    def part1(self):
        self.list_1.sort()
        self.list_2.sort()
            
        return sum([abs(x_1 - x_2) for x_1, x_2 in zip(self.list_1, self.list_2)])

    def part2(self):
        occ = dict([(x,[0,0]) for x in set(self.list_1)])

        for x in self.list_1:
            occ[x][0] += 1

        for x in self.list_2:
            if x in occ:
                occ[x][1] += 1

        return sum([key * value[0] * value[1] for key, value in occ.items()])
    
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